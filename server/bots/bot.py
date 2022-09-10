from abc import ABCMeta, abstractmethod


class Bot(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def call(self, user_msg):
        """
        :param user_msg: last user chat message
        :return: generated string
        """
