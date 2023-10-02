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
        basic =  [m.strip() for m in msg.lower().split('.') if len(m)]
        return basic
        # end_sentence_delim = ['!', '?', '.']
        # end_tokens_indices = [msg.rfind(token) for token in end_sentence_delim]
        # end_tokens_indices = list(filter(lambda x: x >= 0, end_tokens_indices))
        # if end_tokens_indices:
        #     offset = max(end_tokens_indices) + 1
        #     if offset == len(msg):
        #
        #     return [msg[:offset], msg[offset:].strip()]
        # else:
        #     return [msg]


