from bot_server import BotServer

'''
Notice this code use the google translation without a mock - be aware of usage consumption 
'''
server = BotServer("goldfish")
guid = server.register(2)

while True:
    rsp = server.call_bot(guid, input('user: '), {'r': 2, 'c': 23})
    for r in rsp:
        print(f'bot: {r}')
