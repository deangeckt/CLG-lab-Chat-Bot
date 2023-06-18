import re
from typing import Tuple
from pkg_resources import resource_filename
import json
from bots.bot import Bot
from bots.gpt.openai_util import openai_call


class GptBotInstructor(Bot):
    def __init__(self, map_id):
        super().__init__()
        self.chat = []

        kb_path = resource_filename('bots', f'gpt/ins_kw.json')
        with open(kb_path, 'r') as f:
            kb = json.load(f)

        map_kw = kb[f'{map_id}']

        system_prefix1 = kb['system_common_prefix1']
        system_suffix1 = kb['system_common_suffix1']
        system_suffix2 = kb['system_common_suffix2']

        system_map_prefix = kb['system_common_map_prefix']


        system_content = f'{system_prefix1}\n{system_map_prefix}\n{map_kw}\n{system_suffix1}\n{system_suffix2}'
        self.messages = [
            {"role": "system", "content": system_content},
        ]


    def call(self, user_msg, user_state=None) -> Tuple[list[str], bool]:
        self.messages.append({'role': 'user', 'content': user_msg})
        msg, resp = openai_call(self.messages)
        if resp:
            self.messages.append({'role': 'assistant', 'content': msg})
        return [msg], False

    def db_push(self) -> dict:
        # chat is too long for DB
        # return {'chat': self.messages}
        return {}

    def db_load(self, data):
        pass
        # self.messages = []
        # for chat_ele in data['chat']:
        #     self.messages.append({'role': chat_ele['role'], 'content': chat_ele['content']})
