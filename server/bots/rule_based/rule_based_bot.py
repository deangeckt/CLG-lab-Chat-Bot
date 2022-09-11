from pkg_resources import resource_filename
from bots.bot import Bot
import json

from bots.rule_based.template_matchers.greetings import Greetings
from bots.rule_based.template_matchers.single_object_location import SingleObjectLocation
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare
from bots.rule_based.template_matchers.two_objects_proximity import TwoObjectsProximity


class ruleBasedBot(Bot):
    def __init__(self):
        super().__init__()
        self.chat = []
        kb_path = resource_filename('bots', 'rule_based/map_kb.json')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)

        template_matchers_inputs = TemplateMatcherShare(self.kb)
        self.ordered_template_matchers = [Greetings(template_matchers_inputs),
                                          TwoObjectsProximity(template_matchers_inputs),
                                          SingleObjectLocation(template_matchers_inputs)]

    def __state_machine(self, user_msg):
        for template_matcher in self.ordered_template_matchers:
            is_match = template_matcher.match(user_msg)
            if is_match is not None:
                return is_match

        return 'hmm'

    def call(self, user_msg):
        self.chat.append({'speaker': 'user', 'text': user_msg})
        bot_msg = self.__state_machine(user_msg)
        self.chat.append({'speaker': 'bot', 'text': bot_msg})
        return bot_msg
