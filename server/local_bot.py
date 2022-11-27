from bot_server import BotServer

server = BotServer()
guid = server.register()

while True:
    rsp = server.call_bot(guid, input('user: '), {'r': 2, 'c': 23})
    for r in rsp:
        print(f'bot: {r}')
