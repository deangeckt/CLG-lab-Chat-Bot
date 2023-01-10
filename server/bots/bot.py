from abc import ABCMeta, abstractmethod


class Bot(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, user_msg, user_state=None) -> list[str]:
        """
        param user_msg: last user chat message
        param user_state: current coordinate of user on the map
        :return: generated string in a list
        """
