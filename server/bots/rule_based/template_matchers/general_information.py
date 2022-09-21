import math
import re
import random

from bots.rule_based.template_matchers.single_object_location import SingleObjectLocation
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
        self.engaged = False
        self.closest_obj = None
        self.next_direction = None
        self.strategies = [self.__informative1, self.__informative2, self.__engage_question]
        self.strategies_wo_engage = [self.__informative1, self.__informative2]
        self.single_obj_loc_matcher = SingleObjectLocation(share)

    @staticmethod
    def __is_match(text):
        t = text.lower()
        match = bool(re.match("(where (to|now))(.*)", t))
        match |= bool(re.match("(where should i (go|head))(.*)", t))
        match |= bool(re.match("(i (do not|don't) know)(.*)", t))
        return match

    def __informative1(self):
        """
        e.g. 'keep going <direction>'
        e.g. next direction given from the KB
        """
        direction_mapping = {'right': ['east', 'right'],
                             'left': ['west', 'left'],
                             'up': ['north', 'up'],
                             'down': ['south', 'down'],
                             }

        direction_phrase = random.choice(direction_mapping[self.next_direction])
        main_verb = random.choice(GeneralInformation.verb_options)
        return f'{main_verb} {direction_phrase}'

    def __get_direction_phrase(self, direction_word):
        direction_phrase = direction_word
        if direction_phrase in self.shared.prepositions_directions:
            direction_phrase += ' the'
        else:
            direction_phrase += ' by the'

        return direction_phrase

    def __informative2(self):
        """
        e.g. 'keep going <direction> by the <object>'
        :return: random phrasing of informative statement
        """
        direction_word = random.choice(self.shared.direction_mapping[self.next_direction])
        direction_phrase = self.__get_direction_phrase(direction_word)
        main_verb = random.choice(GeneralInformation.verb_options)
        return f'{main_verb} {direction_phrase} {self.closest_obj}'

    def __engage_question(self):
        self.engaged = True
        return f'do you see the {self.closest_obj}?'

    def __find_closest_object(self, user_coord):
        min_dist = 1000
        closest_obj = ''
        for obj in self.shared.kb_abs:
            r = self.shared.kb_abs[obj]['r']
            c = self.shared.kb_abs[obj]['c']
            obj_coord = (r, c)
            curr_dist = math.dist(user_coord, obj_coord)
            if curr_dist < min_dist:
                min_dist = curr_dist
                closest_obj = obj
        return closest_obj

    def match(self, user_msg, user_state=None):
        if user_state is None:
            return

        if self.engaged:
            self.engaged = False
            if 'yes' in user_msg:
                response = self.__informative1()
                return f'{response} from it'
            elif 'no' in user_msg:
                return self.single_obj_loc_matcher.match(f'where is the {self.closest_obj}')

        is_match = self.__is_match(user_msg)
        if not is_match:
            return None

        self.closest_obj = self.__find_closest_object((user_state['r'], user_state['c']))
        if self.closest_obj == 'treasure':
            return 'you found the treasure!'
        self.next_direction = random.choice(self.shared.kb_abs[self.closest_obj]['next_direction'])
        if self.next_direction in self.shared.direction_mapping:
            if self.closest_obj in ['start']:
                strategy = random.choice(self.strategies_wo_engage)
            else:
                strategy = random.choice(self.strategies)
            return strategy()
        else:
            return self.next_direction
