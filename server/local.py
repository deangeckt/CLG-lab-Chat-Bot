from bots.rule_based.match_utils import *
from bots.rule_based.rule_based_bot import ruleBasedBot
from bots.rule_based.template_utils import *

chat_bot = ruleBasedBot()
while True:
    rsp = chat_bot.call(input('user: '))
    print(f'bot: {rsp}')

print(informative_statement1('elephant', 'pil', 'right'))
print(informative_statement1('elephant', 'pil', 'left'))
print(informative_statement1('elephant', 'pil', 'up'))
print(informative_statement2('elephant', 'up'))
print(informative_statement2('elephant', 'down'))
print(informative_statement3('down'))
print(informative_statement3('down'))

print(is_greeting('hey there!'))
print(is_greeting('Hello there!'))
print(is_question('Hello there'))
