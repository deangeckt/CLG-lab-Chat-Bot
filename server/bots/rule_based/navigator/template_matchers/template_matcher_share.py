import math
import re
import string
import random
from time import sleep


class TemplateMatcherShare:
    def __init__(self, kb, chat):
        self.chat = chat
        self.kb_abs = kb['absolute']
        self.kb_path_order = list(self.kb_abs.keys())

        self.where_to_suffix = ["where should i go?", "where should i go now?",
                                "where do i need to go?",
                                "where do i have to go?",
                                "which direction should i take?",
                                "which direction should i go now?"
                                ]

        self.finish = False
        self.state_pth_idx = 0
        self.next_state_idx = 1
        self.next_state_obj = ''

    def update_state(self):
        if self.finish:
            return
        self.next_state_idx = self.state_pth_idx + 1
        self.next_state_obj = self.kb_path_order[self.next_state_idx]

    def advance_state_path(self, adv):
        # sleep(1)
        self.state_pth_idx += adv
        if self.state_pth_idx == len(self.kb_path_order) - 1:
            self.finish = True

    def obj_is_ahead(self):
        options = [
            "i have not reached the",
            "i didn't pass the",
            "i did not pass the",
            "i have not been at the",
            "i didn't walked through the"
        ]
        opt = random.choice(options)
        prefix = random.choice(["it's pretty far, ", 'but ', ''])
        return [f"{prefix}{opt} {self.next_state_obj} yet"]

    @staticmethod
    def obj_is_behind(obj_match):
        options = [
            "i have already passed by the",
            "i have already passed the",
            "i have already been at the",
            "i have already walked through the",
        ]
        opt = random.choice(options)
        return [f"{opt} {obj_match}"]
