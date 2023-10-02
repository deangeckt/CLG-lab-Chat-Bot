import random
from abc import ABCMeta, abstractmethod
from typing import Tuple


class Bot(metaclass=ABCMeta):
    welcome_options = ['hola, q tal? empezamos el juego?',
                       'hola, estas listo?',
                       'hola!!! ya comenzamos?',
                       'hey there, estas listo?',
                       'hola, you ready?',
                       'hi there, empezamos?',
                       'hola, q tal? ready to go?',
                       'hola, q tal? ready to start?',
                       'hola, q tal? ready to play?',
                       'hi there! que comience el juego!!'
                       ]

    def __init__(self):
        self.welcome_str = random.choice(Bot.welcome_options)
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

    @staticmethod
    def informal_post_process(msg: str) -> list[str]:
        # return a list with up to 2 messages split by '.'
        messages =  [m.strip() for m in msg.lower().split('.') if len(m)]
        if len(messages) > 2:
            mid = int(len(messages) / 2)
            return ['. '.join(messages[:mid]), '. '.join(messages[mid:])]

        return messages
