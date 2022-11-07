import re
import random
from typing import Union

from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class EndMatcher(TemplateMatcher):
    """
    e.g.: 'where is the end?' -> ‘the end is some object in the map, you should follow’
    """
    end_response = [['the end is some object on the map', 'you should follow my orders to reach it'],
                    ["the end is some object on the map", "i'll instruct you through"]
                    ]
    goal_response = [
        ['the goal is to reach some object on the map in a specific path',
         'you should follow my orders to reach it'],
        ['the goal is to reach some object on the map in a specific path',
         "i'll instruct you through"],
    ]

    @staticmethod
    def __is_end_match(text):
        t = text.lower()
        match = bool(re.match("(.*)((where|what) is the (end))(.*)", t))
        return match

    @staticmethod
    def __is_goal_match(text):
        t = text.lower()
        match = bool(re.match("(.*)(what is the goal?)(.*)", t))
        return match

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        if self.__is_end_match(user_msg):
            return random.choice(EndMatcher.end_response)
        elif self.__is_goal_match(user_msg):
            return random.choice(EndMatcher.goal_response)
        else:
            return None
