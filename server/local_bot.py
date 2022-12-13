from bot_server import BotServer

server = BotServer("goldfish")
guid = server.register(2)

while True:
    rsp = server.call_bot(guid, input('user: '), {'r': 2, 'c': 23})
    for r in rsp:
        print(f'bot: {r}')
