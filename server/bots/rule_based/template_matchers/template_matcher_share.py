from bots.rule_based.template_matchers.match_utils import tokenize


class TemplateMatcherShare:
    def __init__(self, kb):
        print('init kb')
        self.kb = kb
        self.all_objects = set()
        for obj in self.kb:
            self.all_objects.add(obj)
            for dir_ in self.kb[obj]:
                self.all_objects = self.all_objects.union(set(self.kb[obj][dir_]))

    def get_objects_in_user_msg(self, user_msg):
        detected_objects = []
        for token in tokenize(user_msg):
            if token in self.all_objects:
                detected_objects.append(token)

        return detected_objects
