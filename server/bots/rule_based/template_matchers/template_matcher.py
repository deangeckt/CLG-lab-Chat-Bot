from abc import abstractmethod, ABC
from bots.rule_based.template_matchers.template_matcher_share import TemplateMatcherShare


class TemplateMatcher(ABC):
    def __init__(self, share: TemplateMatcherShare):
        self.shared = share
        self.kb = self.shared.kb
        self.chat = self.shared.chat

    @abstractmethod
    def match(self, user_msg):
        """
        param user_msg: last user chat message
        :return: generated template string in case of a match, else None
        """
