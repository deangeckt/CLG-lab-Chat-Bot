import re
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
from bots.rule_based.template_utils import direction_mapping_to_phrasing


class TwoObjectsProximity(TemplateMatcher):
    """
    e.g. "does the parrot is near the elephant?" -> yes
    """
    directions_words_binary = ['located', 'near', 'next to', 'beside']
    directions_words = ['right', 'left', 'right', 'below', 'above',
                        'north', 'south', 'west', 'east']

    @staticmethod
    def __get_direction_in_yn_question(text):
        t = text.lower()
        all_dir_words = TwoObjectsProximity.directions_words.copy()
        all_dir_words.extend(TwoObjectsProximity.directions_words_binary)
        for dir_word in all_dir_words:
            if bool(re.match(f"(.*)(is|does|do the)(.*)({dir_word}(.*))", t)):
                return dir_word
        return False

    @staticmethod
    def __phrasing_yn_dir_to_map(dir_word):
        """
        param dir_word: direction word as part of a user templated yn question
        returned from get_direction_in_yn_question()
        :return: mapping of the dir word: right, left, up down or binary
        """
        if dir_word in TwoObjectsProximity.directions_words_binary:
            return 'binary'
        for mapping in direction_mapping_to_phrasing:
            if dir_word == mapping:
                return mapping
            if dir_word in direction_mapping_to_phrasing[mapping]:
                return mapping
        raise "can't find direction mapping!"

    def match(self, user_msg):
        yn_direction = self.__get_direction_in_yn_question(user_msg)
        detected_objects = self.get_objects_in_user_msg(user_msg)

        if not yn_direction or len(detected_objects) < 2:
            return None

        direction = self.__phrasing_yn_dir_to_map(yn_direction)
        first_obj = detected_objects[0]
        second_obj = detected_objects[1]
        if direction is not 'binary':
            return 'yes' if second_obj in self.kb[first_obj][direction] else 'no'
        else:
            for dir_ in self.kb[first_obj]:
                if dir_ == 'on':
                    continue
                if second_obj in self.kb[first_obj][dir_]:
                    return 'yes'
            return 'no'

