from bot_server import BotServer
from google_cloud.translate import Translate

Translate.__wrapped__.translate_to_eng = lambda self, x: x
Translate.__wrapped__.translate_to_spa = lambda self, x: x

server = BotServer("goldfish")
guid = server.register(2)


while True:
    rsp = server.call_bot(guid, input('user: '), {'r': 2, 'c': 23})
    for r in rsp:
        print(f'bot: {r}')