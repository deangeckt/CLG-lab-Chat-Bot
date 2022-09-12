from pkg_resources import resource_filename
from bots.bot import Bot
import json

from bots.rule_based.template_matchers.general_information import GeneralInformation
from bots.rule_based.template_matchers.greetings import Greetings
from bots.rule_based.template_matchers.single_object_location import SingleObjectLocation
from bots.rule_based.template_matchers.single_object_on import SingleObjectOn
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare
from bots.rule_based.template_matchers.two_objects_proximity import TwoObjectsProximity


class ruleBasedBot(Bot):
    def __init__(self):
        super().__init__()
        self.chat = []
        kb_path = resource_filename('bots', 'rule_based/map_kb.json')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)

        shared = TemplateMatcherShare(self.kb, self.chat)
        self.ordered_template_matchers = [Greetings(shared),
                                          TwoObjectsProximity(shared),
                                          SingleObjectLocation(shared),
                                          SingleObjectOn(shared),
                                          GeneralInformation(shared)]

    def __match_and_respond(self, user_msg, user_state=None):
        for template_matcher in self.ordered_template_matchers:
            resp = template_matcher.match(user_msg, user_state)
            if resp is not None:
                return resp

        return "i'm not sure"

    def call(self, user_msg, user_state=None):
        self.chat.append({'speaker': 'user', 'text': user_msg})
        bot_msg = self.__match_and_respond(user_msg, user_state)
        self.chat.append({'speaker': 'bot', 'text': bot_msg})
        return bot_msg
