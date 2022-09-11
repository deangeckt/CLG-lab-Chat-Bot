import re
import random
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
from bots.rule_based.template_matchers.template_utils import get_direction_phrase


class SingleObjectLocation(TemplateMatcher):
    """
    e.g. "where is the tiger" -> 'the tiger is above the parrot'
    """
    directions_words_binary = ['located', 'near', 'next to', 'beside']
    directions_words = ['right', 'left', 'right', 'below', 'above',
                        'north', 'south', 'west', 'east']

    @staticmethod
    def __is_match(text):
        t = text.lower()
        match = bool(re.match("(.*)(where is|are the)(.*)", t))
        match |= bool(re.match("(.*)(where should the)(.*)", t))
        match |= bool(re.match("(.*)(i do not | don't see the)(.*)", t))
        return match

    def match(self, user_msg):
        detected_objects = self.shared.get_objects_in_user_msg(user_msg)
        is_match = self.__is_match(user_msg)

        if not is_match or len(detected_objects) != 1:
            return None
        obj = detected_objects[0]
        direction = random.choice(list(self.kb[obj].keys()))
        next_obj = random.choice(self.kb[obj][direction])

        direction_phrase = get_direction_phrase(direction)
        return f'the {obj} is {direction_phrase} {next_obj}'
