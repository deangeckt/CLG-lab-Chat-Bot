import uuid
from bots.rule_based.rule_based_bot import RuleBasedBot
from code_switch.code_switch_unit import CodeSwitchUnit
from google_cloud.translate import Translate


class BotServer:
    def __init__(self, cs_strategy: str):
        self.sessions = {}
        self.translate = Translate()
        self.cs_strategy = cs_strategy

    def register(self, map_index, guid=None):
        if guid is None:
            guid = str(uuid.uuid4())

        map_id = f'map_{map_index + 1}'
        self.sessions[guid] = {'bot': RuleBasedBot(map_id),
                               'cs': CodeSwitchUnit(self.cs_strategy)}
        return guid

    def un_register(self, guid):
        del self.sessions[guid]

    def call_bot(self, guid, user_msg, map_idx, user_state=None):
        if guid not in self.sessions:
            print('guid not in self!')
            self.register(map_index=map_idx, guid=guid)

        en_user_msg = self.translate.translate_to_eng(user_msg)
        en_bot_resp = self.sessions[guid]['bot'].call(en_user_msg, user_state)
        spanglish_bot_resp = self.sessions[guid]['cs'].call(user_msg, en_bot_resp)
        return spanglish_bot_resp
