import random
from typing import Union
from bots.rule_based.navigator.template_matchers.template_matcher import TemplateMatcher
from bots.rule_based.shared_utils import is_question

class Direction(TemplateMatcher):
    dir_words = ['west', 'east', 'north', 'south', 'up', 'down', 'right', 'left']
    map_dir = {'west': 'left', 'east': 'right', 'north': 'up', 'south': 'down'}

    def match(self, user_msg) -> Union[list[str], None]:
        if is_question(user_msg):
            return None

        matches = []
        for dir_word in self.dir_words:
            if dir_word in user_msg:
                matches.append(dir_word)

        if not matches:
            return None

        print('match: direction matcher: ', matches)
        for match in matches:
            if match in self.map_dir:
                match = self.map_dir[match]

            axis = 'c' if match in ['right', 'left'] else 'r'
            adv = -3 if match in ['left', 'up'] else 3
            self.shared.advance_state_path(axis, adv)

        prefix = random.choice(self.shared.moved_prefix)
        return [f'{prefix} {self.shared.next_state_obj}']

