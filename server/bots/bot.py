from abc import ABCMeta, abstractmethod
from typing import Tuple


class Bot(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, user_msg, user_state=None) -> Tuple[list[str], bool]:
        """
        param user_msg: last user chat message
        param user_state: current coordinate of user on the map (instructor bot only)
        :return: generated string in a list, flag if the bot has finished (navigator bot only)
        """
    @abstractmethod
    def db_push(self) -> dict:
        """
        push state memory of the bot to DB
        return dict of state memory
        """
        pass

    @abstractmethod
    def db_load(self, data):
        """
        load / override state memory of the bot from DB
        """
        pass
