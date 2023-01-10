from datetime import datetime
from typing import List
from google.cloud import datastore
from singleton_decorator import singleton

@singleton
class Database:
    def __init__(self):
        self.client = datastore.Client()
        self.kind = 'sync'

    def load_cs_state(self, guid):
        key = self.client.key(self.kind, guid)
        ent = self.client.get(key)
        if ent is None:
            return None
        cs_history = ent['cs_history'].split('_')
        len_of_current_subsequence = ent['len_of_current_subsequence']
        return {'cs_history': cs_history, 'len_of_current_subsequence': len_of_current_subsequence}

    def save_cs_state(self, guid, cs_history: List[str], len_of_current_subsequence: int):
        key = self.client.key(self.kind, guid)
        ent = datastore.Entity(key)
        ent['cs_history'] = '_'.join(cs_history)
        ent['len_of_current_subsequence'] = len_of_current_subsequence
        ent['time'] = datetime.now()
        self.client.put(ent)
