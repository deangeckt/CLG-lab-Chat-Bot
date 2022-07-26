import random
import re
from typing import Union
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class Near(TemplateMatcher):
    """
    very general regex! keep last in the matcher list
    e.g. "im near the parrot" -> <next direction suggestion from abs kb>
    """

    def is_match(self, text):
        t = text.lower()
        for obj in self.shared.all_objects:
            if bool(re.match(f"((.*)(i'm|im|i am|i) (.*) the {obj}(.*))", t)):
                return obj
            elif bool(re.match(f"((.*)(near|on|at) the {obj}(.*))", t)):
                return obj
            elif bool(re.match(f"((.*)(the|a) {obj}(.*))", t)):
                return obj
        return False

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        if user_state is None:
            return None
        obj_match = self.is_match(user_msg)
        if not obj_match:
            return None

        print('near matcher')

        # 1st priority - use the object in the user text
        if obj_match in self.shared.kb_abs:
            return [random.choice(self.shared.kb_abs[obj_match]['next_direction'])]

        # 2nd priority - use the closest object of the user
        if obj_match in self.shared.outside_path:
            resp = [f'the {obj_match} is not part of the path']
            closest_obj_indx = self.shared.kb_path_order.index(self.shared.closest_obj)
            next_obj_in_path = self.shared.kb_path_order[closest_obj_indx + 1]
            resp.append(f'go towards the {next_obj_in_path}')
            return resp

        return None
