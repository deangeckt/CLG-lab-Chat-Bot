import json
import random
from dataclasses import dataclass
from typing import List

import langid

from code_switch.utils import hazard

LANG_CODES = {'en': 'eng', 'es': 'spa'}
langid.set_languages(langs=['es', 'en'])


@dataclass()
class CSOption:
    probability: float
    transitions: dict
    r: List[float]


class CodeSwitchUnit:
    def __init__(self, cs_strategy: str):
        self.params = {
            "eng": CSOption(probability=0.7, transitions={'spa': 1.0},
                            r=[0, 0.6, 0.2, 0.1, 0.5, 0.5]),
            "spa": CSOption(probability=0.3, transitions={'eng': 1.0},
                            r=[0, 0.8, 0.15, 0.5])
        }

        self.cs_strategy = cs_strategy
        self.cs_history = []
        self.current_cs_state = None
        self.len_of_current_subsequence = 1
        self.user_msg = None
        self.strategy = {'goldfish': self.__goldfish_cs_strategy,
                         'random': self.__random_strategy}

    def call(self, user_msg: str, en_bot_resp: List[str]) -> List[str]:
        """
        param user_msg: last user chat message in spanglish
        param en_bot_resp: the generated messages (list) the bot generated in english
        :return: spanglish generated string in a list
        """
        self.user_msg = user_msg
        self.__identify_incoming_cs_state()
        new_cs_state = self.__predict_next_cs_state()
        self.__update_cs_state(new_cs_state)
        # HERE GOES THE TRANSLATION OF THE CHATBOT's RESPONSE!!!
        return en_bot_resp

    def __identify_incoming_cs_state(self):
        identified_lang_langid = langid.classify(self.user_msg)[0]
        self.current_cs_state = LANG_CODES[identified_lang_langid]

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


def test_codeswitchunit():
    cs_strategy = "goldfish"
    csunit = CodeSwitchUnit(cs_strategy)

    for _ in range(3):
        user_msg = "me gusta comer sushi"
        csunit.call(user_msg, en_bot_resp=["nice!"])
        user_msg = "it is nice to live in america"
        csunit.call(user_msg, en_bot_resp=["nice!"])
    print(csunit.cs_history)



def run_tests():
    test_codeswitchunit()


if __name__ == '__main__':
    run_tests()
    print("success!")