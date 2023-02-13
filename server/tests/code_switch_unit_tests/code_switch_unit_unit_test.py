import os
os.chdir('../../code_switch')

from code_switch.code_switch_unit import CodeSwitchUnit

strategy = 'random'

csu = CodeSwitchUnit(strategy)

resp = csu.call(guid='0000',user_msg='where should i go next?',
                en_bot_resp=['hi there, how do you do?', 'go north, and then go up above the gorilla'])
print(resp)

resp = csu.call(guid='0000',user_msg='¿Adónde debo ir después?',
                en_bot_resp=['hi there, how do you do?', 'go north, and then go up above the gorilla'])
print(resp)
