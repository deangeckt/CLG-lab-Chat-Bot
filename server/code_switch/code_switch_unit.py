import json


class CodeSwitchUnit:
    def __init__(self, params_file_name, cs_strategy):
        """ Fill it up"""
        self.params = CSParameters(params_file_name)
        self.cs_strategy = cs_strategy

        self.cs_history = []
        self.current_cs_state = None

    def call(self, user_msg: str, en_bot_resp: list[str]):
        """
        param user_msg: last user chat message in spanglish
        param en_bot_resp: the generated messages (list) the bot generated in english
        :return: spanglish generated string in a list
        """
        return en_bot_resp

    def predict_next_cs_state(self):
        if self.current_cs_state == None:  #not-initialized
            pass

        elif self.cs_strategy == 'goldfish':
            pass

        elif self.cs_strategy == 'random':
            pass

        else:
            pass

    def update_cs_state(self, new_state):
        self.current_cs_state = new_state
        self.cs_history.append(new_state)

    def goldfish_cs_strategy(self):
        pass

    def random_strategy(self):
        pass


def test_codeswitchunit():
    param_file_name = "cs_parameters.txt"
    cs_strategy = "goldfish"
    csunit = CodeSwitchUnit(param_file_name, cs_strategy)
    csunit.predict_next_cs_state()
    print(csunit.current_cs_state)


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

        self.states_options = {}
        self.load_parameters()

    def load_parameters(self):
        with open(self.param_file_name) as f:
            variables = json.load(f)

        for lang, params in variables.items():

            transitions = {}
            for param_name, param in params.items():
                if param_name == "p":
                    p = params["p"]
                elif param_name == "r":
                    r = params["r"]
                else:
                    transitions[param_name] = param

            self.states_options[lang] = CSOption(
                state_name=lang, p=p, transitions=transitions, r=r)


def test_csparameters():
    param_file_name = "cs_parameters.txt"
    params = CSParameters(param_file_name)
    for cs_state, cs_params in params.states_options.items():
        print(cs_params)



def run_tests():
    test_csparameters()
    test_codeswitchunit()


if __name__ == '__main__':
    run_tests()
    print("success!")