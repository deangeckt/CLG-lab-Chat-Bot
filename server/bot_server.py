import uuid
from typing import Tuple

from bots.bot import Bot
from code_switch.cs_unit import CSUnit
from google_cloud.database import Database
from google_cloud.translate import Translate

# from bots.rule_based.rule_based_bot_ins import RuleBasedBotInstructor
# from bots.rule_based.rule_based_bot_nav import RuleBasedBotNavigator
# from code_switch.netzer.code_switch_unit import CodeSwitchUnit
from bots.gpt.gpt_bot_nav import GptBotNavigator
from bots.gpt.gpt_bot_ins import GptBotInstructor
from bots.gpt.gpt_cs import GPTCodeSwitch




class BotServer:
    def __init__(self):
        self.sessions = {}
        self.translate = Translate()
        self.database = Database()

    def register(self, map_index, game_role, guid=None):
        if guid is None:
            guid = str(uuid.uuid4())
        map_id = f'map_{map_index + 1}'
        bot: Bot = GptBotNavigator(map_id) if game_role == 1 else GptBotInstructor(map_id)
        self.sessions[guid] = {'bot': bot,
                               'cs': GPTCodeSwitch()}
        return guid

    def un_register(self, guid):
        if guid in self.sessions:
            del self.sessions[guid]

    def call_bot(self, guid, user_msg, map_idx, game_role, user_state=None) -> Tuple[list[str], bool]:
        en_user_msg = self.translate.translate_to_eng(user_msg)

        db_data = None
        if guid not in self.sessions:
            print('guid not in self! getting DB')
            self.register(map_index=map_idx, game_role=game_role, guid=guid)
            # db_data = self.database.load(guid)

        bot: Bot = self.sessions[guid]['bot']
        cs_unit: CSUnit = self.sessions[guid]['cs']

        # if db_data is not None:
        #     print('db: ', db_data)
        #     cs_unit.db_load(db_data)
        #     bot.db_load(db_data)

        en_bot_resp, is_finish = bot.call(en_user_msg, user_state)
        spanglish_bot_resp = cs_unit.call(user_msg, en_bot_resp)

        # push to DB when call is finished
        # data = cs_unit.db_push()
        # data.update(bot.db_push())
        # self.database.push(data, guid)

        return spanglish_bot_resp, is_finish
