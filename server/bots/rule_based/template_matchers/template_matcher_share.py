import math
import re
import string
from typing import Union


class TemplateMatcherShare:
    def __init__(self, kb, chat):
        self.chat = chat

        self.kb_abs = kb['absolute']
        self.kb_path_order = list(self.kb_abs.keys())
        self.start_object = self.kb_path_order[0]
        self.goal_object = self.kb_path_order[-1]
        self.outside_path = kb['outside_path']

        self.all_objects = set(self.kb_path_order)
        self.all_objects = self.all_objects.union(set(self.outside_path))

        self.closest_obj = None

    def find_closest_object(self, user_coord):
        """
        return the closest obj to the user coord - only objects from the abs KB!
        """
        min_dist = 1000
        closest_obj = ''
        for obj in self.kb_abs:
            r = self.kb_abs[obj]['r']
            c = self.kb_abs[obj]['c']
            obj_coord = (r, c)
            curr_dist = math.dist(user_coord, obj_coord)
            if curr_dist < min_dist:
                min_dist = curr_dist
                closest_obj = obj
        self.closest_obj = closest_obj

    def is_closest_object_on_map_obj(self, user_coord) -> Union[str, None]:
        self.find_closest_object(user_coord)
        if self.closest_obj == self.start_object:
            return None
        r = self.kb_abs[self.closest_obj]['r']
        c = self.kb_abs[self.closest_obj]['c']
        closest_obj_coord = (r, c)
        curr_dist = math.dist(user_coord, closest_obj_coord)
        return self.closest_obj if curr_dist < 2 else None

    @staticmethod
    def tokenize(text):
        text = text.strip().lower()
        split = re.findall(fr'[${string.punctuation}]|\w+', text)
        return [t for t in split]
