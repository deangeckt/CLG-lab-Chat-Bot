from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
import random
import re


class Greetings(TemplateMatcher):
    greeting_words = {'hi', 'hello', 'hey', 'hiya', 'howdy'}
    basic_options = ['hey there', 'hello there', 'hi', 'hey', 'hello']
    how_are_you_options = ['all well thank you!', 'very well thanks', "i'm good thank you"]

    def __is_basic_greeting(self, text):
        for token in self.shared.tokenize(text):
            if token in Greetings.greeting_words:
                return True
        return False

    @staticmethod
    def __is_how_are_you_greeting(text):
        t = text.lower()
        match = bool(re.match("(.*)(are you today)(.*)", t))
        match |= bool(re.match("(how are you)(.*)", t))
        match |= bool(re.match("(.*)(you doing)(.*)", t))
        match |= bool(re.match("(.*)(going on)(.*)", t))
        return match

    def match(self, user_msg, user_state=None):
        if self.__is_basic_greeting(user_msg):
            return random.choice(Greetings.basic_options)
        elif self.__is_how_are_you_greeting(user_msg):
            return random.choice(Greetings.how_are_you_options)
        else:
            return None
