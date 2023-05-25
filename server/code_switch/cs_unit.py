from abc import ABCMeta, abstractmethod
from typing import List


class CSUnit(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, user_msg: str, en_bot_resp: List[str]) -> List[str]:
        """
        param user_msg: last user chat message
        param en_bot_resp: the generated messages (list) the bot generated in english
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
