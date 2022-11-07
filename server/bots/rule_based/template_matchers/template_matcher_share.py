import math
import re
import string


class TemplateMatcherShare:
    angle_directions = ['east', 'west', 'south', 'north']
    prepositions_directions = ['above', 'below']
    direction_mapping = {'right': ['east', 'right'],
                         'left': ['west', 'left'],
                         'up': ['north', 'above'],
                         'down': ['south', 'below'],
                         'on': ['on']}

    def __init__(self, kb, chat):
        self.chat = chat
        self.kb_prox = kb['proximity']
        self.kb_abs = kb['absolute']
        self.kb_path_order = kb['order']
        self.all_objects = set()

        for obj in self.kb_prox:
            self.all_objects.add(obj)
            for dir_ in self.kb_prox[obj]:
                self.all_objects = self.all_objects.union(set(self.kb_prox[obj][dir_]))
        print(self.all_objects)

    def get_objects_in_user_msg(self, user_msg):
        detected_objects = []
        for token in self.tokenize(user_msg):
            if token in self.all_objects:
                detected_objects.append(token)
        return detected_objects

    def find_closest_object(self, user_coord):
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
        return closest_obj

    @staticmethod
    def tokenize(text):
        text = text.strip().lower()
        split = re.findall(fr'[${string.punctuation}]|\w+', text)
        return [t for t in split]

    @staticmethod
    def get_direction_phrase(direction_word):
        direction_phrase = direction_word
        if direction_phrase in TemplateMatcherShare.angle_directions:
            direction_phrase += ' of the'
        elif direction_phrase in ['above', 'below']:
            direction_phrase += ' the'
        else:
            direction_phrase += ' to the'

        return direction_phrase
