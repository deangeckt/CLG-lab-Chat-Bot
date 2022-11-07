import random
import re
from typing import Union
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class Near(TemplateMatcher):
    """
    e.g. "im near the parrot" -> <next direction suggestion from abs kb>
    """

    def is_match(self, text):
        t = text.lower()
        for obj in self.shared.all_objects:
            if bool(re.match(f"((.*)(i'm|im|i am) (near|on|at) the {obj}(.*))", t)):
                return obj
        return False

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        if user_state is None:
            return None
        obj_match = self.is_match(user_msg)
        if not obj_match:
            return None

        resp = []

        if obj_match not in self.shared.kb_path_order:
            resp.append(f'the {obj_match} is not part of the path')
            closest_obj = self.shared.find_closest_object((user_state['r'], user_state['c']))
            closest_obj_indx = self.shared.kb_path_order.index(closest_obj)
            next_obj_in_path = self.shared.kb_path_order[closest_obj_indx + 1]
            resp.append(f'go towards the {next_obj_in_path}')
        else:
            if obj_match in self.shared.kb_abs:
                general_dir_from_closest_obj = self.shared.kb_abs[obj_match]['next_direction']
                resp.append(random.choice(general_dir_from_closest_obj))
            else:
                obj_match_indx = self.shared.kb_path_order.index(obj_match)
                next_obj_in_path = self.shared.kb_path_order[obj_match_indx + 1]
                resp.append(f'awsome, go towards the {next_obj_in_path}')

        return resp
