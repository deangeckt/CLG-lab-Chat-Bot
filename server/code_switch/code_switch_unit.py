import json
import random
import langid

from utils import *

LANG_CODES = {'en': 'eng', 'es': 'spa'}
langid.set_languages(langs=['es', 'en'])


class CodeSwitchUnit:
    def __init__(self, params_file_name, cs_strategy):
        """ Fill it up"""
        self.params = CSParameters(params_file_name)
        self.cs_strategy = cs_strategy

        self.cs_history = []
        self.current_cs_state = None
        self.len_of_current_subsequence = 1

        self.user_msg = None

    def call(self, user_msg: str, en_bot_resp: list[str]):
        """
        param user_msg: last user chat message in spanglish
        param en_bot_resp: the generated messages (list) the bot generated in english
        :return: spanglish generated string in a list
        """
        self.user_msg = user_msg
        self.identify_incoming_cs_state()
        new_cs_state = self.predict_next_cs_state()
        self.update_cs_state(new_cs_state)
        # HERE GOES THE TRANSLATION OF THE CHATBOT's RESPONSE!!!
        return en_bot_resp

    def identify_incoming_cs_state(self):
        identified_lang_langid = langid.classify(self.user_msg)[0]
        self.current_cs_state = LANG_CODES[identified_lang_langid]

    def predict_next_cs_state(self):
        if self.current_cs_state is None:  # not-initialized
            new_state = self.random_strategy()

        elif self.cs_strategy == 'goldfish':
            new_state = self.goldfish_cs_strategy()

        elif self.cs_strategy == 'random':
            new_state = self.random_strategy()

        else:
            new_state = self.random_strategy()

        return new_state

    def update_cs_state(self, new_state):
        self.current_cs_state = new_state
        self.cs_history.append(new_state)

    def goldfish_cs_strategy(self):
        r = self.params.states_options_dict[self.current_cs_state].r
        p = hazard(r, s=self.len_of_current_subsequence)
        res = random.choices([True, False], [p, 1 - p])[0]
        if res:  # change state
            next_state = self.select_next_state(self.current_cs_state)
            self.len_of_current_subsequence = 1
        else:  # keep current state
            next_state = self.current_cs_state
            self.len_of_current_subsequence += 1
        return next_state

    def select_next_state(self, current_state):
        all_next_possible_state_options = []
        all_next_possible_state_probabilities = []
        for next_state_option, next_state_transition_probability in \
                self.params.states_options_dict[current_state].transitions.items():

            if not(next_state_option == current_state):
                all_next_possible_state_options.append(next_state_option)
                all_next_possible_state_probabilities.append(next_state_transition_probability)
        next_state = random.choices(all_next_possible_state_options, all_next_possible_state_probabilities)[0]
        return next_state

    def random_strategy(self):
        weights = []
        lang_options = self.params.state_options
        for lang in lang_options:
            cs_option = self.params.states_options_dict[lang]
            p = cs_option.p
            weights.append(p)
        return random.choices(lang_options, weights)[0]


def test_codeswitchunit():
    param_file_name = "cs_parameters.txt"
    cs_strategy = "goldfish"
    csunit = CodeSwitchUnit(param_file_name, cs_strategy)

    csunit.predict_next_cs_state()
    for _ in range(3):
        user_msg = "me gusta comer sushi"
        csunit.call(user_msg, en_bot_resp="nice!")
        user_msg = "it is nice to live in america"
        csunit.call(user_msg, en_bot_resp="nice!")
    print(csunit.cs_history)


class CSOption(object):
    def __init__(self, state_name, p, transitions, r):
        self.state_name = state_name
        self.p = p
        self.transitions = transitions
        self.r = r  # relative portion of constant state length = r(d=k)

    def __str__(self):
        s = ""
        s += "The state " + self.state_name + '\n'
        s += "raw probability {}".format(self.p) + '\n'
        return s


class CSParameters(object):
    def __init__(self, param_file_name):
        self.param_file_name = param_file_name
        self.state_options = []
        self.states_options_dict = {}
        self.load_parameters()

    def load_parameters(self):
        with open(self.param_file_name) as f:
            variables = json.load(f)

        for lang, params in variables.items():
            self.state_options.append(lang)
            transitions = {}
            for param_name, param in params.items():
                if param_name == "p":
                    p = params["p"]
                elif param_name == "r":
                    r = params["r"]
                else:
                    transitions[param_name] = param

            self.states_options_dict[lang] = CSOption(
                state_name=lang, p=p, transitions=transitions, r=r)


def test_csparameters():
    param_file_name = "cs_parameters.txt"
    params = CSParameters(param_file_name)
    for cs_state, cs_params in params.states_options_dict.items():
        print(cs_params)


def run_tests():
    test_csparameters()
    test_codeswitchunit()


if __name__ == '__main__':
    run_tests()
    print("success!")