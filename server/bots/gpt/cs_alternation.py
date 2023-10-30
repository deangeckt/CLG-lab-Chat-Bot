from typing import List

from bots.cs_unit import CSUnit, CodeSwitchStrategy
from bots.lang_id_bert import LangIdBert, LanguageId
from google_cloud.translate import Translate
import random


class CodeSwitchAlternation(CSUnit):
    """
    This unit alternate by translating a whole sentence given a strategy
    """
    SHORT_CTX = 3
    def __init__(self, strategy: CodeSwitchStrategy, welcome_str: str):
        super().__init__()
        self.lid = LangIdBert()
        self.translate = Translate()
        self.cs_history: list[LanguageId] = [self.lid.identify(welcome_str)]

        self.strategy = strategy
        self.strategies = {
            CodeSwitchStrategy.none: self.__none_call,
            CodeSwitchStrategy.alternation_random: self.__random_call,
            CodeSwitchStrategy.alternation_short_context: self.__short_context_call,
            CodeSwitchStrategy.alternation_switch_last_user: self.__switch_last_user_call
        }

        self.is_last_switched = False

    def __random_call(self, _: str, bot_resp: List[str]) -> List[str]:
        """
        on the Turn level - i.e.: can translate more than one utterance
        """
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

    def __short_context_call(self, _: str, bot_resp: List[str]) -> List[str]:
        """
        on the utterance lvl - Translate only last one in the turn
        """
        bot_langs = [self.lid.identify(msg) for msg in bot_resp]
        self.cs_history.extend(bot_langs)

        if len(self.cs_history) < CodeSwitchAlternation.SHORT_CTX:
            return bot_resp

        if self.cs_history[-1] == LanguageId.mix:
            return bot_resp

        last_langs = self.cs_history[-CodeSwitchAlternation.SHORT_CTX:]
        last_langs_set = set(last_langs)
        if LanguageId.mix in last_langs_set:
            last_langs_set.remove(LanguageId.mix)
        if len(last_langs_set) > 1:
            return bot_resp


        self.is_last_switched = True

        lang = self.cs_history[-1]
        translate_cb = self.translate.translate_to_spa if lang == LanguageId.eng else self.translate.translate_to_eng

        switch_lang = LanguageId.es if lang == LanguageId.eng else LanguageId.eng
        self.cs_history[-1] = switch_lang

        last_resp = bot_resp[-1]
        bot_resp[-1] = translate_cb(last_resp)

        return bot_resp

    @staticmethod
    def __none_call(_: str, bot_resp: List[str]) -> List[str]:
        return bot_resp

    def __switch_last_user_call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        """
        on the Turn level - i.e.: can translate more than one utterance
        """
        user_lng = self.lid.identify(user_msg)
        if user_lng == LanguageId.mix:
            return bot_resp

        translate_cb = self.translate.translate_to_spa if user_lng == LanguageId.eng else self.translate.translate_to_eng
        bot_resp_translated = [translate_cb(msg) for msg in bot_resp]
        self.is_last_switched = True
        return bot_resp_translated


    def call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        self.is_last_switched = False
        callback = self.strategies[self.strategy]
        return callback(user_msg, bot_resp)

    def is_switched(self) -> bool:
        return self.is_last_switched

    def db_push(self) -> dict:
        pass

    def db_load(self, data):
        pass