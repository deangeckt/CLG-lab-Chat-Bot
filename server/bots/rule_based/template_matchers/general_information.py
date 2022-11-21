import re
import random
from typing import Union

from bots.rule_based.engage import engage_next
from bots.rule_based.template_matchers.template_matcher import TemplateMatcher
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare


class GeneralInformation(TemplateMatcher):
    """
    e.g.: 'where should I go now?' -> pick next direction from KB abs’
    e.g.: nav: 'where should I go now?', 'ins': engage question , nav: at /near at/ the X, ins: NEAR matcher'
    """

    def __init__(self, share: TemplateMatcherShare):
        super().__init__(share)

    @staticmethod
    def __is_match(text):
        t = text.lower()
        match = bool(re.match("(.*)(where (to|now))(.*)", t))
        match |= bool(re.match("(where should i (go|head))(.*)", t))
        match |= bool(re.match("(now (what| where)?)", t))
        match |= bool(re.match("(where do i go)(.*)", t))
        match |= bool(re.match("(i (do not|don't) know)(.*)", t))
        match |= bool(re.match("(.*)(now?)", t))
        match |= bool(re.match("(ok now (what|where)(.*))", t))
        match |= bool(re.match("(.*)(how to continue?)", t))
        match |= bool(re.match("(.*)(what next?)", t))
        match |= bool(re.match("(where)", t))
        return match

    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        if user_state is None:
            return

        is_match = self.__is_match(user_msg)
        if not is_match:
            return None

        print('general matcher')

        if random.random() > 0.5:
            return [random.choice(self.shared.kb_abs[self.shared.closest_obj]['next_direction'])]
        else:
            return [f'ok, {engage_next()}']
