from bot_server import BotServer
from google_cloud.database import Database
from google_cloud.translate import Translate

def db_mock():
    pass


Translate.__wrapped__.translate_to_eng = lambda self, x: x
Translate.__wrapped__.translate_to_spa = lambda self, x: x
Database.__wrapped__.save_cs_state = lambda self, g, x, y: db_mock()

server = BotServer("goldfish")
guid = server.register(0)


while True:
    rsp = server.call_bot(guid=guid, user_msg=input('user: '), map_idx=0, user_state={'r': 5, 'c': 11})
    for r in rsp:
        print(f'bot: {r}')