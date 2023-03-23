from bot_server import BotServer
from google_cloud.database import Database
from google_cloud.translate import Translate

def db_mock():
    pass


Translate.__wrapped__.translate_to_eng = lambda self, x: x
Translate.__wrapped__.translate_to_spa = lambda self, x: x
Database.__wrapped__.push = lambda self, data_, guid_: db_mock()

server = BotServer("goldfish")
game_role = 0
guid = server.register(map_index=0, game_role=game_role)
while True:
    rsp, is_finish = server.call_bot(guid=guid, user_msg=input('user: '),
                                     map_idx=0,
                                     game_role=game_role,
                                     user_state={'r': 3, 'c': 9})
    for r in rsp:
        print(f'bot: {r}')
    if is_finish:
        print('Bot finished!')
        break