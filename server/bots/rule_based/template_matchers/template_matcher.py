from abc import abstractmethod, ABC
from typing import Union

from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare


class TemplateMatcher(ABC):
    def __init__(self, share: TemplateMatcherShare):
        self.shared = share
        self.kb_prox = self.shared.kb_prox
        self.chat = self.shared.chat

    @abstractmethod
    def match(self, user_msg, user_state=None) -> Union[list[str], None]:
        """
        param user_msg: last user chat message
        param user_state: current coordinate of user on the map
        :return: generated template string in case of a match, else None
        """
