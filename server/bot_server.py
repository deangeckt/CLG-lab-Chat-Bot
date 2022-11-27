import uuid

from bots.rule_based.rule_based_bot import ruleBasedBot


class BotServer:
    def __init__(self):
        self.sessions = {}

    def register(self):
        guid = str(uuid.uuid4())
        chat_bot = ruleBasedBot()
        self.sessions[guid] = chat_bot
        return guid

    def un_register(self, guid):
        del self.sessions[guid]

    def call_bot(self, guid, user_msg, user_state=None):
        return self.sessions[guid].call(user_msg, user_state)

    def call_bot_loc(self, guid, user_state=None):
        return self.sessions[guid].location_move(user_state)
