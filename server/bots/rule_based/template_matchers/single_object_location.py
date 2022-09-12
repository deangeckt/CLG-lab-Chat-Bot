import re
import random
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class SingleObjectLocation(TemplateMatcher):
    """
    e.g. "where is the tiger" -> 'the tiger is above the parrot'
    e.g. "I don't see the tiger" -> 'the tiger is above the parrot'
    """

    @staticmethod
    def __is_match(text):
        t = text.lower()
        match = bool(re.match("(.*)(where is|are the)(.*)", t))
        match |= bool(re.match("(.*)(where should the)(.*)", t))
        match |= bool(re.match("(.*)(i do not | don't see the)(.*)", t))
        return match

    def __get_direction_phrase(self, direction_word):
        direction_phrase = direction_word
        if direction_phrase in self.shared.angle_directions:
            direction_phrase += ' of the'
        elif direction_phrase in self.shared.prepositions_directions or direction_phrase == 'on':
            direction_phrase += ' the'
        else:
            direction_phrase += ' to the'

        return direction_phrase

    def match(self, user_msg, user_state=None):
        detected_objects = self.shared.get_objects_in_user_msg(user_msg)
        is_match = self.__is_match(user_msg)

        if not is_match or len(detected_objects) != 1:
            return None
        obj = detected_objects[0]
        if obj not in self.kb_prox:
            return None

        direction = random.choice(list(self.kb_prox[obj].keys()))
        direction_word = random.choice(self.shared.direction_mapping[direction])
        next_obj = random.choice(self.kb_prox[obj][direction])

        direction_phrase = self.__get_direction_phrase(direction_word)
        return f'the {obj} is {direction_phrase} {next_obj}'
