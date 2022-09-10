from enum import Enum
from pkg_resources import resource_filename
from bots.bot import Bot
import json
from bots.rule_based.match_utils import *

from bots.rule_based.template_utils import *


class UserCategory(Enum):
    greeting = 1
    simple_answer = 2
    map_obj_wh_question = 3
    map_obj_yn_question = 4
    map_obj_statement = 5
    question = 6
    statement = 7


class BotCategory(Enum):
    greeting = 1
    simple_answer = 2
    informative_statement = 3
    engage_question = 4
    path_statement = 5


class ruleBasedBot(Bot):
    def __init__(self):
        super().__init__()
        self.chat = []
        kb_path = resource_filename('bots', 'rule_based/map_kb.json')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)

        self.objects = self.kb.keys() # TODO remove start as an object?

    def __get_category(self, user_msg):
        if is_greeting(user_msg):
            return UserCategory.greeting
        if is_simple_answer(user_msg):
            return UserCategory.simple_answer

        question = is_question(user_msg)
        map_obj = is_map_object_included(user_msg, self.objects)

        if map_obj:
            if question == 'wh':
                return UserCategory.map_obj_wh_question
            elif question == 'yn':
                return UserCategory.map_obj_yn_question
            else:
                return UserCategory.map_obj_statement
        else:
            if question != 'none':
                return UserCategory.question
            else:
                return UserCategory.statement

    def __state_machine(self, user_msg, category):
        if category == UserCategory.greeting:
            return greetings(), BotCategory.greeting
        return 'bot', BotCategory.greeting

    def call(self, user_msg):
        user_category = self.__get_category(user_msg)
        print(user_category.name)
        self.chat.append({'speaker': 'user', 'text': user_msg, 'category': user_category.name})
        bot_msg, bot_category = self.__state_machine(user_msg, user_category)
        self.chat.append({'speaker': 'bot', 'text': bot_msg, 'category': bot_category.name})
        return bot_msg
