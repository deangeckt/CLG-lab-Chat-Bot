import re
import random
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare


class GeneralInformation(TemplateMatcher):
    """
    e.g.: 'where should I go now?' -> ‘continue left by the water’
    e.g.: 'I don’t know where to go'-> ‘continue left by the water’
    """
    verb_options = ['keep going', 'continue']

    def __init__(self, share: TemplateMatcherShare):
        super().__init__(share)
        self.strategies = [self.__informative1, self.__informative2, self.__engage_question]

    @staticmethod
    def __is_match(text):
        t = text.lower()
        match = bool(re.match("(where (to|now))(.*)", t))
        match |= bool(re.match("(where should i (go|head))(.*)", t))
        match |= bool(re.match("(i (do not|don't) know)(.*)", t))
        return match

    @staticmethod
    def __informative1(_, direction):
        """
        e.g. 'keep going <direction>'
        :param direction: up, down, right, left
        :return: random phrasing of informative statement
        """
        direction_mapping = {'right': ['east', 'right'],
                             'left': ['west', 'left'],
                             'up': ['north', 'up'],
                             'down': ['south', 'down'],
                             }

        direction_phrase = random.choice(direction_mapping[direction])
        main_verb = random.choice(GeneralInformation.verb_options)
        return f'{main_verb} {direction_phrase}'

    def __get_direction_phrase(self, direction_word):
        direction_phrase = direction_word
        if direction_phrase in self.shared.prepositions_directions:
            direction_phrase += ' the'
        else:
            direction_phrase += ' by the'

        return direction_phrase

    def __informative2(self, obj, direction):
        """
        e.g. 'keep going <direction> to / by the <object>'
        :param obj: an object from the kb
        :param direction: up, down, right, left - without on
        :return: random phrasing of informative statement
        """
        direction_word = random.choice(self.shared.direction_mapping[direction])
        direction_phrase = self.__get_direction_phrase(direction_word)
        main_verb = random.choice(GeneralInformation.verb_options)
        return f'{main_verb} {direction_phrase} {obj}'

    @staticmethod
    def __engage_question(obj, _):
        """
        e.g. 'do you see the <obj>'
        :param obj: an object from the kb
        :return: engaging question
        """
        return f'do you see the {obj}?'

    def match(self, user_msg):
        is_match = self.__is_match(user_msg)
        if not is_match:
            return None

        # TODO use state to determine those
        obj = 'tiger'
        direction = 'right'

        strategy = random.choice(self.strategies)
        return strategy(obj, direction)
