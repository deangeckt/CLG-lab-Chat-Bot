from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List

class CodeSwitchStrategy(str, Enum):
    none = "none"
    alternation_random = "alternation_random"
    alternation_short_context = "alternation_short_context_uter"
    alternation_switch_last_user = "alternation_switch_last_user"
    alternation_align_last_user = "alternation_align_last_user"


class CSUnit(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, user_msg: str, bot_resp: List[str]) -> List[str]:
        """
        param user_msg: last user chat message
        param bot_resp: the generated messages (list) the bot generated in (can be in either language)
        :return: spanglish generated string in a list
        """
    @abstractmethod
    def db_push(self) -> dict:
        """
        push state memory of the cs unit to DB
        return dict of state memory
        """
        pass

    @abstractmethod
    def db_load(self, data):
        """
        load / override state memory of the cs unit from DB
        """
        pass

    @abstractmethod
    def is_switched(self):
        """
        is last bot msg switched with some sort of CS strategy
        """
        pass