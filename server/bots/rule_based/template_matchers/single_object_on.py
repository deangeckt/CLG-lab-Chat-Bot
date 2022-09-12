import re
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

    def match(self, user_msg, user_state=None):
        obj_match = self.is_match(user_msg)
        if not obj_match:
            return None
        on_item = user_msg.lower().split('on')[-1].strip()
        on_item = on_item.split('the')[-1].strip()
        on_item = on_item.split('?')[0]
        return 'yes' if on_item in self.kb_prox[obj_match]['on'] else 'no'
