import uuid
from bots.rule_based.rule_based_bot import RuleBasedBot
from code_switch.code_switch_unit import CodeSwitchUnit
from google.cloud import translate
import html

translate_client = translate.TranslationServiceClient()
parent = f"projects/dialogue-362312"


class BotServer:
    def __init__(self):
        self.sessions = {}

    def register(self):
        guid = str(uuid.uuid4())
        self.sessions[guid] = {'bot': RuleBasedBot('map_1'),
                               'cs': CodeSwitchUnit()}
        return guid

    def un_register(self, guid):
        del self.sessions[guid]

    def call_bot(self, guid, user_msg, user_state=None):
        en_user_msg = self.__translate_to_eng(user_msg)
        print(en_user_msg)
        en_bot_resp = self.sessions[guid]['bot'].call(en_user_msg, user_state)
        spanglish_bot_resp = self.sessions[guid]['cs'].call(user_msg, en_bot_resp)
        return spanglish_bot_resp

    def call_bot_loc(self, guid, user_state=None):
        return self.sessions[guid]['bot'].location_move(user_state)

    @staticmethod
    def __translate_to_eng(user_msg):
        response = translate_client.translate_text(
            contents=[user_msg],
            source_language_code='es',
            target_language_code='en',
            parent=parent,
        )
        translated_text = response.translations[0].translated_text
        return html.unescape(translated_text)
