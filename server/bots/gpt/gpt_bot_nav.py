import re
from typing import Tuple
from pkg_resources import resource_filename
import json
from bots.bot import Bot
from bots.gpt.openai_util import openai_call


class GptBotNavigator(Bot):
    def __init__(self, map_id):
        super().__init__()
        self.chat = []

        kb_path = resource_filename('bots', f'gpt/ins_kw.json')
        with open(kb_path, 'r') as f:
            kb = json.load(f)

        map_kw = kb[f'{map_id}']
        map_suffix_kw = kb[f'{map_id}_suffix']

        system_prefix1 = kb['system_common_prefix1']
        system_prefix2 = kb['system_common_prefix2']
        system_suffix = kb['system_common_suffix1']
        system_map_prefix = kb['system_common_map_prefix']

        self.final_object = kb[f'{map_id}_final_object']

        system_content = f'{system_prefix1}\n{system_prefix2}\n{system_map_prefix}\n{map_kw}\n{map_suffix_kw}\n{system_suffix}'
        self.messages = [
            {"role": "system", "content": system_content},
        ]

    def __is_finished(self, bot_resp: str):
        t = bot_resp.lower()
        if 'finished' in t: return True
        match = bool(re.match(f"(.*)(reached the {self.final_object})(.*)", t))
        return match


    def call(self, user_msg, user_state=None) -> Tuple[list[str], bool]:
        self.messages.append({'role': 'user', 'content': user_msg})
        msg, resp = openai_call(self.messages)
        if resp:
            self.messages.append({'role': 'assistant', 'content': msg})
        return [msg], self.__is_finished(msg)

    def db_push(self) -> dict:
        return {}

    def db_load(self, data):
        pass