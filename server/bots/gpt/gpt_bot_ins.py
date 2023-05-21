from typing import Tuple

from pkg_resources import resource_filename
import json
import random

from bots.bot import Bot
from bots.rule_based.instructor.template_matchers.clarification import Clarification
from bots.rule_based.instructor.template_matchers.done import Done
from bots.rule_based.instructor.template_matchers.game_instructions import GameInstructions
from bots.rule_based.instructor.template_matchers.general_information import GeneralInformation
from bots.rule_based.instructor.template_matchers.goal import GoalMatcher
from bots.rule_based.instructor.template_matchers.greetings import Greetings
from bots.rule_based.instructor.template_matchers.near import Near
from bots.rule_based.instructor.template_matchers.template_matcher_share import TemplateMatcherShare
from bots.rule_based.instructor.template_matchers.towards import Towards
from bots.rule_based.shared_utils import find_closest_object


class GptBotInstructor(Bot):
    def __init__(self, map_id):
        super().__init__()
        self.chat = []

        kb_path = resource_filename('bots', f'rule_based/maps_kb/{map_id}.json')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)


    def call(self, user_msg, user_state=None) -> Tuple[list[str], bool]:
        self.chat.append({'speaker': 'user', 'text': user_msg})
        bot_msgs = self.__match_and_respond(user_msg, user_state)
        bot_msgs = [m.capitalize() for m in bot_msgs]
        for bot_msg in bot_msgs:
            self.chat.append({'speaker': 'bot', 'text': bot_msg})
        return bot_msgs, False

    def db_push(self) -> dict:
        return {}

    def db_load(self, data):
        pass