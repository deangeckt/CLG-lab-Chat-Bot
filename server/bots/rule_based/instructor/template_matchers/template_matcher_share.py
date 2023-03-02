import random

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


    def get_kb_suggestion(self, object_) -> list[str]:
        curr_suggestion = random.choice(self.kb_abs[object_]['next_direction'])
        return [curr_suggestion] if type(curr_suggestion) == str else curr_suggestion
