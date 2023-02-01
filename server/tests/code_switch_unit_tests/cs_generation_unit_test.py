import os
os.chdir('../../code_switch')

import json

from code_switch.generation.en_generation import ENGeneration
from code_switch.generation.et_generation import ETGeneration
from code_switch.generation.el_generation import ELGeneration
from code_switch.generation.ep_generation import EPGeneration
from code_switch.generation.sn_generation import SNGeneration
from code_switch.generation.st_generation import STGeneration
from code_switch.generation.sl_generation import SLGeneration
from code_switch.generation.sp_generation import SPGeneration

from google_cloud.translate import Translate

translate = Translate()

en = ENGeneration()
et = ETGeneration(list_of_spanish_starts=['bien...', 'amigo,', 'mi amigo,'])
el = ELGeneration(translation_pairs=json.loads(open('resources/translation_pairs.json', 'r').read()))
ep = EPGeneration(translate)
sp = SPGeneration(translate)
sl = SLGeneration(translate, translation_pairs=json.loads(open('resources/translation_pairs.json', 'r').read()))
st = STGeneration(translate, list_of_english_starts=['well...', 'oh well,', 'let me think...'])
sn = SNGeneration(translate)


bot_response_spanglish, actual_cs_level = en.generate(bot_response_english='i love you!')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = et.generate(bot_response_english='i love you!')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = el.generate(bot_response_english='i love you!')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = el.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = ep.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = sp.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = sl.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = st.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)

bot_response_spanglish, actual_cs_level = sn.generate(bot_response_english='go back from the start and continue north')
print("Response: " + bot_response_spanglish)
print("Actual CS level: " + actual_cs_level)