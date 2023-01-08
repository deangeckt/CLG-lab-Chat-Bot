from pkg_resources import resource_filename
from bots.bot import Bot
import json
import random
from bots.rule_based.template_matchers.clarification import Clarification
from bots.rule_based.template_matchers.done import Done
from bots.rule_based.template_matchers.goal import GoalMatcher
from bots.rule_based.template_matchers.game_instructions import GameInstructions
from bots.rule_based.template_matchers.general_information import GeneralInformation
from bots.rule_based.template_matchers.greetings import Greetings
from bots.rule_based.template_matchers.near import Near
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare
from bots.rule_based.template_matchers.towards import Towards


class RuleBasedBot(Bot):
    def __init__(self, map_id):
        super().__init__()
        self.chat = []
        self.no_resp_prefix = ["i'm not sure what you mean but maybe this will help:",
                               "not too sure about that, but maybe this will help:"]

        kb_path = resource_filename('bots', f'rule_based/maps_kb/{map_id}.json')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)

        shared = TemplateMatcherShare(self.kb, self.chat)
        self.shared = shared
        self.ordered_template_matchers = [
            GameInstructions(shared),
            GoalMatcher(shared),
            Greetings(shared),
            Clarification(shared),
            Done(shared),
            GeneralInformation(shared),
            Towards(shared),
            Near(shared),
        ]

    def __match_and_respond(self, user_msg, user_state=None) -> list[str]:
        try:
            self.shared.find_closest_object((user_state['r'], user_state['c']))

            if self.shared.closest_obj == self.shared.goal_object:
                return [random.choice([f'you are close to the {self.shared.goal_object}!, head over there!',
                                       f'you are near the {self.shared.goal_object}, go to it!'])]

            for template_matcher in self.ordered_template_matchers:
                resp = template_matcher.match(user_msg, user_state)
                if resp is not None:
                    return resp

            default_msg = [random.choice(self.no_resp_prefix)]
            default_msg.extend(self.shared.get_kb_suggestion(self.shared.closest_obj))
            return default_msg


        except Exception as e:
            print('err:', e)

        return [random.choice(["i'm not sure", "i'm not 100% sure"])]

    def call(self, user_msg, user_state=None) -> list[str]:
        self.chat.append({'speaker': 'user', 'text': user_msg})
        bot_msgs = self.__match_and_respond(user_msg, user_state)
        bot_msgs = [m.capitalize() for m in bot_msgs]
        for bot_msg in bot_msgs:
            self.chat.append({'speaker': 'bot', 'text': bot_msg})
        return bot_msgs
