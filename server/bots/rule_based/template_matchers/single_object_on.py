import re
from typing import Union

from bots.rule_based.template_matchers.template_matcher import TemplateMatcher


class SingleObjectOn(TemplateMatcher):
    """
    e.g. "is the tiger on the green island?" -> yes
    """
    def is_match(self, text):
        t = text.lower()
        for obj in self.shared.all_objects:
            if bool(re.match(f"((is|does|do) the {obj} on(.*))", t)):
                return obj
        return False

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        obj_match = self.is_match(user_msg)
        if not obj_match:
            return None
        if obj_match not in self.kb_prox:
            return None
        on_item = user_msg.lower().split('on')[-1].strip()
        on_item = on_item.split('the')[-1].strip()
        actual_on = self.kb_prox[obj_match]['on'][0]
        if actual_on in on_item or on_item in actual_on or on_item.split('?')[0] in actual_on:
            return ['yes']
        return ['no']
