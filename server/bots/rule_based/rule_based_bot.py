import math
import random

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


class ruleBasedBot(Bot):
    def __init__(self):
        super().__init__()
        self.chat = []
        self.visited_on = {}
        self.no_resp_prefix = ["i'm not sure but maybe this will help:",
                               "hmm not too sure about that, but maybe this will help:"]

        kb_path = resource_filename('bots', 'rule_based/map_kb.json')
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

            return [random.choice(self.no_resp_prefix),
                    random.choice(self.shared.kb_abs[self.shared.closest_obj]['next_direction'])]

        except Exception as e:
            print('err:', e)

        return ["i'm not sure"]

    def __append_bot_messages(self, bot_msgs: list[str]):
        for bot_msg in bot_msgs:
            self.chat.append({'speaker': 'bot', 'text': bot_msg})

    def call(self, user_msg, user_state=None) -> list[str]:
        self.chat.append({'speaker': 'user', 'text': user_msg})
        bot_msgs = self.__match_and_respond(user_msg, user_state)
        self.__append_bot_messages(bot_msgs)
        return bot_msgs

    def location_move(self, user_state) -> list[str]:
        on_map_obj = self.shared.is_closest_object_on_map_obj((user_state['r'], user_state['c']))
        if on_map_obj is None:
            return []
        if on_map_obj in self.visited_on:
            return []

        self.visited_on[on_map_obj] = 1
        prefix_options = ['well done', 'nice', 'awsome']
        prefix = random.choice(prefix_options)
        bot_msgs = [f'{prefix}! you have reached the {on_map_obj}']
        self.__append_bot_messages(bot_msgs)
        return bot_msgs
