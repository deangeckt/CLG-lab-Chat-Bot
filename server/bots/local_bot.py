from bots.rule_based.rule_based_bot import ruleBasedBot

chat_bot = ruleBasedBot()
while True:
    rsp = chat_bot.call(input('user: '), {'r': 15, 'c': 2})
    for r in rsp:
        print(f'bot: {r}')
