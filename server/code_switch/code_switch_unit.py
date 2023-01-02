import random
from dataclasses import dataclass
from typing import List
from google_cloud.database import Database
from google_cloud.translate import Translate
import langid
from code_switch.utils import hazard

langid.set_languages(langs=['es', 'en'])


@dataclass()
class CSOption:
    probability: float
    transitions: dict
    r: List[float]


class CodeSwitchUnit:
    def __init__(self, cs_strategy: str):
        self.params = {
            "en": CSOption(probability=0.7, transitions={'es': 1.0},
                            r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
            "es": CSOption(probability=0.3, transitions={'en': 1.0},
                            r=[0, 0.8, 0.15, 0.5])
        }
        self.cs_strategy = cs_strategy
        self.default_lang = 'en'
        self.user_msg = None
        self.strategy = {'goldfish': self.__goldfish_cs_strategy,
                         'random': self.__random_strategy,
                         'tit_for_tat': self.__tit_for_tat_strategy,
                         'english_only': self.__english_only_strategy,
                         'spanish_only': self.__spanish_only_strategy
                        }

        self.translate = Translate()
        self.database = Database()
        self.translation = {'en': lambda x: x,
                            'es': self.translate.translate_to_spa}

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
            new_cs_state = self.__predict_next_cs_state()
            self.__update_cs_state(new_cs_state)
            spanglish_bot_response = self.translation[new_cs_state](eng_resp)
            spanglish_bot_response_list.append(spanglish_bot_response)
        return spanglish_bot_response_list

    def __identify_incoming_cs_state(self):
        self.current_cs_state = langid.classify(self.user_msg)[0]

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
        return 'en'

    @staticmethod
    def __spanish_only_strategy():
        return 'es'


