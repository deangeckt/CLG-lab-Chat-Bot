from bot_server import BotServer
from code_switch.code_switch_unit import CodeSwitchUnit
from google_cloud.database import Database
from google_cloud.translate import Translate

user_state_mock = {'r': 2, 'c': 23}
user_msg_mock = [("how are you?", "¿cómo estás?", "¿cómo estás?"),
                 ("where should i go?", "¿A donde debería ir?", "¿A donde debería ir?"),
                 ("where should i go?", "¿A donde debería ir?", "where should i go?")
                 ]
en_to_sp_translations = {"how are you?": "¿cómo estás?",
                         "where should i go?": "¿A donde debería ir?",
                        "ok, what do you see in front of you now?": "Bien, ¿qué ves frente a ti ahora?",
                        "i'm good thank you": "estoy bien gracias",
                        "go across the bridge towards the tiger": "cruzar el puente hacia el tigre",
                        "ok, now, what is in front of you?": "Bien, ahora, ¿qué hay delante de ti?",
                        "go left on the branches on the water": "vaya a la izquierda en las ramas en el agua",
                        "go left towards the tiger":"ir a la izquierda hacia el tigre",
                        "all well thank you!":"todo bien gracias!",
                        "ok, where are you now?":"¿OK donde estas ahora?"
                         }
to_en_translations = {"¿cómo estás?": "how are you?",
                      "¿A donde debería ir?": "where should i go?",
                      "where should i go?": "where should i go?"
                      }

def translate_to_en_mock(msg: str) -> str:
    if msg in to_en_translations:
        return to_en_translations[msg]
    print(f'log: translate to en oov: "{msg}"')
    return msg

def translate_to_sp_mock(msg: str) -> str:
    if msg in en_to_sp_translations:
        return en_to_sp_translations[msg]
    print(f'log: translate to sp oov: "{msg}"')
    return msg

def db_mock():
    pass

def run_mock_chat(strategy: str):
    Translate.__wrapped__.translate_to_eng = lambda self, user_msg: translate_to_en_mock(user_msg)
    Translate.__wrapped__.translate_to_spa = lambda self, en_msg: translate_to_sp_mock(en_msg)
    Database.__wrapped__.save_cs_state = lambda self, g, x, y: db_mock()

    print('strategy:', strategy)
    server = BotServer(cs_strategy=strategy)
    guid = server.register(map_index=0)

    for msg in user_msg_mock:
        english_msg, spanish_msg, spanglish_msg = msg
        print('user:', spanglish_msg)
        rsp = server.call_bot(guid=guid, user_msg=spanglish_msg, map_idx=0, user_state=user_state_mock)
        for r in rsp:
            print('bot:', r)

    print('cs history: ', server.sessions[guid]['cs'].cs_history)
    print('\n')

if __name__ == '__main__':
    cs = CodeSwitchUnit('i just want the strategy keys of this object')
    for strategy in cs.strategy.keys():
        run_mock_chat(strategy)
