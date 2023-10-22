from typing import List

from bots.cs_unit import CSUnit, CodeSwitchStrategy
from bots.lang_id_bert import LangIdBert, LanguageId
from google_cloud.translate import Translate
import random


class CodeSwitchAlternation(CSUnit):
    """
    This unit alternate by translating a whole sentence given a strategy
    """

    def __init__(self, strategy: CodeSwitchStrategy):
        super().__init__()
        self.cs_history = []

        self.lid = LangIdBert()
        self.translate = Translate()

        self.strategy = strategy
        self.strategies = {
            CodeSwitchStrategy.none: self.__none_call,
            CodeSwitchStrategy.alternation_random: self.__random_call,
            CodeSwitchStrategy.alternation_sequence: self.__sequence_call
        }

        self.is_last_switched = False

    @staticmethod
    def __random_call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        random_factor = 0.5
        if random.random() > random_factor:
            return bot_resp

        bot_langs = [self.lid.identify(msg) for msg in bot_resp]
        if LanguageId.mix in bot_langs:
            return bot_resp

        if len(set(bot_langs)) > 1:
            return bot_resp

        # either all are spanish or english
        lang: LanguageId = bot_langs[0]
        translate_cb = self.translate.translate_to_spa if lang == LanguageId.eng else self.translate.translate_to_eng
        bot_resp_translated = [translate_cb(msg) for msg in bot_resp]
        self.is_last_switched = True
        return bot_resp_translated

    def __sequence_call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        return bot_resp

    @staticmethod
    def __none_call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        return bot_resp

    def call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        self.is_last_switched = False
        callback = self.strategies[self.strategy]
        return callback(self, user_msg, bot_resp)

    def is_switched(self) -> bool:
        return self.is_last_switched

    def db_push(self) -> dict:
        return {'cs_history': '_'.join(self.cs_history)}

    def db_load(self, data):
        self.cs_history = data['cs_history'].split('_')
