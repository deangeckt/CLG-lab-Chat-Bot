from bots.rule_based.match_utils import tokenize
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
import random


class Greetings(TemplateMatcher):
    greeting_words = {'hi', 'hello', 'hey', 'hiya', 'howdy'}
    resp_options = ['hey there', 'hello there', 'hi', 'hey', 'hello']

    # TODO: can add more complicated greetings such as "how are you"

    @staticmethod
    def __is_greeting(text):
        for token in tokenize(text):
            if token in Greetings.greeting_words:
                return True
        return False

    def match(self, user_msg):
        if not self.__is_greeting(user_msg):
            return None

        return random.choice(Greetings.resp_options)
