from unittest.mock import patch
from bot_server import BotServer
from google_cloud.translate import Translate

user_state_mock = {'r': 2, 'c': 23}
user_msg_mock = [("how are you?", "¿cómo estás?", "¿cómo estás?"),

                 ]
en_to_sp_translations = {"how are you?": "¿cómo estás?"}
sp_to_en_translations = {"¿cómo estás?": "how are you?"}


def translate_mock(msg: str) -> str:
    if msg in en_to_sp_translations:
        return en_to_sp_translations[msg]
    elif msg in sp_to_en_translations:
        return sp_to_en_translations[msg]
    return f'cs needed to translate to SP: {msg}'


@patch.object(Translate.__wrapped__, 'translate_to_eng', new=lambda self, user_msg: translate_mock(user_msg))
@patch.object(Translate.__wrapped__, 'translate_to_spa', new=lambda self, en_msg: translate_mock(en_msg))
def test_cs_strategies():

    strategy = 'goldfish'

    server = BotServer(cs_strategy=strategy)
    guid = server.register(map_index=0)

    for msg in user_msg_mock:
        english_msg, spanish_msg, spanglish_msg = msg
        print('user:', spanglish_msg)
        rsp = server.call_bot(guid, spanglish_msg, user_state_mock)
        for r in rsp:
            print('bot:', r)
