import random
import re
from typing import Union
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class Towards(TemplateMatcher):
    """
    e.g. "should I go toward the parrot?" -> yes
    e.g. "should I go toward the parrot?" -> no, <next direction suggestion from abs kb>
    """
    def is_match(self, text):
        t = text.lower()
        for obj in self.shared.all_objects:
            if bool(re.match(f"((should|do) i (continue to|go towards|go to|head to) the {obj}(.*))", t)):
                return obj
        return False

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        if user_state is None:
            return None
        obj_match = self.is_match(user_msg)
        if not obj_match:
            return None

        closest_obj = self.shared.find_closest_object((user_state['r'], user_state['c']))
        if obj_match == 'treasure':
            if closest_obj == 'treasure':
                return ['yes! you found the treasure!']
            else:
                return ['in general yes, but you should follow path instruction']

        if closest_obj not in self.shared.kb_path_order:
            return None

        closest_obj_indx = self.shared.kb_path_order.index(closest_obj)
        next_obj_in_path = self.shared.kb_path_order[closest_obj_indx + 1]

        resp = []

        if obj_match not in self.shared.kb_path_order:
            resp.append(f'the {obj_match} is not part of the path')
        else:
            obj_match_indx = self.shared.kb_path_order.index(obj_match)
            if closest_obj_indx == obj_match_indx - 1:
                return ['yes']

        general_dir_from_closest_obj = self.shared.kb_abs[closest_obj]['next_direction']
        options = [general_dir_from_closest_obj, [f'no, you should go towards the {next_obj_in_path}']]
        resp.append(random.choice(random.choice(options)))
        return resp

