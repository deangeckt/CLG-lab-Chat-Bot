import json
import random
from dataclasses import dataclass
from typing import List
from google_cloud.database import Database
from google_cloud.translate import Translate
import langid
from code_switch.utils import hazard
from cs_level_identification import calc_cs_level

from cs_strategies import RandomStrategy, GoldfishStrategy, TitForTatStrategy, EnglishOnlyStrategy, SpanishOnlyStrategy, DEFAULT_CS_PARAMS
from cs_generation import ENGeneration, ETGeneration, ELGeneration, EPGeneration, SPGeneration, SLGeneration, STGeneration, SNGeneration

LIST_OF_ENGLISH_STARTS = ['well...', 'oh well,', 'let me think...']
LIST_OF_SPANISH_STARTS = ['bien...', 'amigo,', 'mi amigo,']

PUNCTUATIONS_MARKS = ['!', '?', ',', ':', ';', '.']

class CodeSwitchUnit:
	def __init__(self, cs_strategy: str):
		self.params = DEFAULT_CS_PARAMS
		self.translation_pairs = json.loads(open('resources/translation_pairs.json', 'r').read())
		self.cs_strategy = cs_strategy
		self.default_lang = 'EN'
		self.user_msg = None
		self.strategy = {'goldfish': GoldfishStrategy(self.params),
						 'random': RandomStrategy(self.params),
						 'tit_for_tat': TitForTatStrategy(self.params),
						 'english_only': EnglishOnlyStrategy(self.params),
						 'spanish_only': SpanishOnlyStrategy(self.params)
						}

		self.translate = Translate()
		self.database = Database()
		self.generation = {'EN': ENGeneration(),
							'ET': ETGeneration(list_of_spanish_starts=LIST_OF_SPANISH_STARTS),
							'EL': ELGeneration(translation_pairs=self.translation_pairs),
							'EP': EPGeneration(self.translate),
							'SP': SPGeneration(self.translate),
							'SL': SLGeneration(self.translate, translation_pairs=self.translation_pairs),
							'ST': STGeneration(self.translate, list_of_english_starts=LIST_OF_ENGLISH_STARTS),
							'SN': SNGeneration(self.translate)
							}
		# State
		self.cs_history = []
		self.current_cs_state = None
		self.len_of_current_subsequence = 1

	def call(self, guid: str, user_msg: str, en_bot_resp: List[str]) -> List[str]:
		"""
		param guid: id of the session
		param user_msg: last user chat message in spanglish
		param en_bot_resp: the generated messages (list) the bot generated in english
		:return: spanglish generated string in a list
		"""
		self.user_msg = user_msg
		self.__identify_incoming_cs_state()
		resp = self.__generate_response(en_bot_resp)
		self.database.save_cs_state(guid, self.cs_history, self.len_of_current_subsequence)
		return resp

	def override_state_from_db(self, data: dict):
		self.len_of_current_subsequence = data['len_of_current_subsequence']
		self.cs_history = data['cs_history']
		self.current_cs_state = self.cs_history[-1]


	def __generate_response(self, en_bot_resp: List[str]) -> List[str]:
		spanglish_bot_response_list = []
		for eng_resp in en_bot_resp:
			selected_cs_state = self.__predict_next_cs_state()
			spanglish_bot_response, actual_cs_level = self.generation[selected_cs_state].generate(eng_resp)
			self.__update_cs_state(actual_cs_level)
			spanglish_bot_response_list.append(spanglish_bot_response)
		return spanglish_bot_response_list

	def __identify_incoming_cs_state(self):
		# self.current_cs_state = langid.classify(self.user_msg)[0]
		self.current_cs_state = calc_cs_level(self.user_msg)

	def __predict_next_cs_state(self):
		return self.strategy[self.cs_strategy].predict_next_cs_level(self.current_cs_state)

	def __update_cs_state(self, new_state):
		self.current_cs_state = new_state
		self.cs_history.append(new_state)