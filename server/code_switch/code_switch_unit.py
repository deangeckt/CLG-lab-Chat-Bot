import json
import random
from dataclasses import dataclass
from typing import List
from google_cloud.database import Database
from google_cloud.translate import Translate
import langid
from code_switch.utils import hazard
from cs_level_identification import calc_cs_level

PUNCTUATIONS_MARKS = ['!', '?', ',', ':', ';', '.']

@dataclass()
class CSOption:
	probability: float
	transitions: dict
	r: List[float]


class CodeSwitchUnit:
	def __init__(self, cs_strategy: str):
		self.params = {
			"EN": CSOption(probability=0.7,
						   transitions={'ET': 0.1, 'EL': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"ET": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.8, 0.15, 0.5]),
			"EL": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'ET': 0.1,'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"EP": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SP": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SL': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SL": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'ST': 0.1, 'SN': 0.1},
							r=[0, 0.8, 0.15, 0.5]),
			"ST": CSOption(probability=0.7,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'SN': 0.1},
							r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
			"SN": CSOption(probability=0.3,
							transitions={'EN': 0.1, 'EL': 0.1,'ET': 0.1, 'EP': 0.1, 'SP': 0.1, 'SL': 0.1, 'ST': 0.1},
							r=[0, 0.8, 0.15, 0.5])
		}
		self.cs_strategy = cs_strategy
		self.default_lang = 'EN'
		self.user_msg = None
		self.strategy = {'goldfish': self.__goldfish_cs_strategy,
						 'random': self.__random_strategy,
						 'tit_for_tat': self.__tit_for_tat_strategy,
						 'english_only': self.__english_only_strategy,
						 'spanish_only': self.__spanish_only_strategy
						}

		self.translate = Translate()
		self.database = Database()
		self.translation = {'EN': self.__generate_en_response,
							'ET': self.__generate_et_response,
							'EL': self.__generate_el_response,
							'EP': self.__generate_ep_response,
							'SP': self.__generate_sp_response,
							'SL': self.__generate_sl_response,
							'ST': self.__generate_st_response,
							'SN': self.translate.translate_to_spa
							}
		self.translation_pairs = json.loads(open('translation_pairs.json', 'r').read())

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
			spanglish_bot_response, actual_cs_level = self.translation[selected_cs_state](eng_resp)
			self.__update_cs_state(actual_cs_level)
			spanglish_bot_response_list.append(spanglish_bot_response)
		return spanglish_bot_response_list

	def __identify_incoming_cs_state(self):
		# self.current_cs_state = langid.classify(self.user_msg)[0]
		self.current_cs_state = calc_cs_level(self.user_msg)


	def __predict_next_cs_state(self):
		if self.current_cs_state is None:  # not-initialized
			return self.__random_strategy()

		return self.strategy[self.cs_strategy]()

	def __update_cs_state(self, new_state):
		self.current_cs_state = new_state
		self.cs_history.append(new_state)

	def __goldfish_cs_strategy(self):
		r = self.params[self.current_cs_state].r
		p = hazard(r, s=self.len_of_current_subsequence)
		res = random.choices([True, False], [p, 1 - p])[0]
		if res:  # change state
			next_state = self.__select_next_state(self.current_cs_state)
			self.len_of_current_subsequence = 1
		else:  # keep current state
			next_state = self.current_cs_state
			self.len_of_current_subsequence += 1
		return next_state

	def __select_next_state(self, current_state):
		all_next_possible_state_options = []
		all_next_possible_state_probabilities = []
		for next_state_option, next_state_transition_probability in \
				self.params[current_state].transitions.items():

			if not(next_state_option == current_state):
				all_next_possible_state_options.append(next_state_option)
				all_next_possible_state_probabilities.append(next_state_transition_probability)
		next_state = random.choices(all_next_possible_state_options, all_next_possible_state_probabilities)[0]
		return next_state

	def __random_strategy(self):
		weights = []
		for lang in self.params:
			cs_option: CSOption = self.params[lang]
			weights.append(cs_option.probability)
		return random.choices(list(self.params.keys()), weights)[0]

	def __tit_for_tat_strategy(self):
		next_state = self.default_lang
		previous_user_lang = langid.classify(self.user_msg)[0]
		if previous_user_lang is not None:
			next_state = previous_user_lang
		return next_state

	@staticmethod
	def __english_only_strategy():
		return 'EN'

	@staticmethod
	def __spanish_only_strategy():
		return 'SN'

	def __generate_en_response(self, bot_response_english):
		return bot_response_english, 'EN'

	def __generate_et_response(self, bot_response_english):
		es_addition_at_start = random.choices(['bien...', 'amigo', 'mi amigo'])[0]
		return es_addition_at_start + ' ' + bot_response_english

	def __generate_el_response(self, bot_response_english):
		bot_response_el = bot_response_english
		replacement_found = False
		for english_token in self.translation_pairs['en']:
			if bot_response_english.find(english_token) > 0:  # Found in text
				replacement_found = True
				break

		for english_token, spanish_token in zip(self.translation_pairs['en'], self.translation_pairs['es']):
			bot_response_el = bot_response_el.replace(english_token, spanish_token)

		if replacement_found:
			final_cs_level = 'EL'
		else:
			final_cs_level = 'EN'
		return bot_response_el, final_cs_level

	def __generate_ep_response(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'EN'
	
	def __generate_sp_response(self, bot_response_english):
		return self.translate.translate_to_spa(bot_response_english), 'SN'

	def __generate_sl_response(self, bot_response_english):
		bot_response_sl = self.translate.translate_to_spa(bot_response_english)
		replacement_found = False
		for spanish_token in self.translation_pairs['es']:
			if bot_response_sl.find(spanish_token) > 0:  # Found in text
				replacement_found = True
				break

		for spanish_token, english_token in zip(self.translation_pairs['es'], self.translation_pairs['en']):
			bot_response_sl = bot_response_sl.replace(spanish_token, english_token)

		if replacement_found:
			final_cs_level = 'SL'
		else:
			final_cs_level = 'SN'
		return bot_response_sl, final_cs_level

	def __generate_st_response(self, bot_response_english):
		bot_response_spanish = self.translate.translate_to_spa(bot_response_english)
		en_addition_at_start = random.choices(['well...', 'oh well,', 'let me think...'])[0]
		return en_addition_at_start + ' ' + bot_response_spanish, 'ST'
