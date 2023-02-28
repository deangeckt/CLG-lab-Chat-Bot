import random
import re
from time import sleep
from typing import Union
from bots.rule_based.navigator.template_matchers.template_matcher import TemplateMatcher


class Action(TemplateMatcher):
    """
    keep matcher last - very generic
    """
    match_the_words = ['over', 'around', 'surround', 'surrounding', 'near', 'above', 'below', 'beside',
                       'toward', 'towards', 'leave', 'cross', 'from', 'pass', 'on', 'follow', 'of',
                       'where', 'between', 'beneath']

    did_it_prefix = ["ok, i did it, i'm next to the",
                     "awsome! as you said, i'm now near the",
                     'sure, i have reached the',
                     'awsome! i have reached the',
                     ]

    def __is_match(self, text):
        t = text.lower()
        for obj in self.shared.kb_path_order:
            if bool(re.match(f"((.*)to the {obj}(.*))", t)):
                 return True
            elif bool(re.match(f"((.*)({'|'.join(Action.match_the_words)}) the {obj}(.*))", t)):
                return True
        return False

    def match(self, user_msg) -> Union[list[str], None]:
        if not self.__is_match(user_msg):
            return None

        obj_matches = list(filter(lambda obj: obj in user_msg, self.shared.kb_path_order))
        print('match: action matcher: ', obj_matches)

        for obj_match in reversed(obj_matches):
            obj_idx = self.shared.kb_path_order.index(obj_match)
            if obj_idx == self.shared.next_state_idx:
                self.shared.advance_state_path(1)
                prefix = random.choice(Action.did_it_prefix)
                return [f'{prefix} {self.shared.next_state_obj}']
            if obj_idx == self.shared.next_state_idx + 1:
                self.shared.advance_state_path(2)
                prefix = random.choice(Action.did_it_prefix)
                return [f'{prefix} {obj_match}']


        obj_match = obj_matches[-1]
        obj_idx = self.shared.kb_path_order.index(obj_match)

        if obj_idx > self.shared.next_state_idx:
            return self.shared.obj_is_ahead()
        else:
            return self.shared.obj_is_behind(obj_match)
