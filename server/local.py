from bots.rule_based.rule_based_bot import ruleBasedBot

chat_bot = ruleBasedBot()
while True:
    rsp = chat_bot.call(input('user: '), {'x': 0.3, 'y': 0.3})
    print(f'bot: {rsp}')
