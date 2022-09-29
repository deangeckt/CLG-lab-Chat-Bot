import queue
import uuid
from collections import defaultdict


class Server:
    def __init__(self):
        self.sessions_roles = [{}]
        self.sessions_resp = {}
        self.listeners = defaultdict(list)

    @staticmethod
    def __format_sse(data: str):
        msg = f'data: {data}\n\n'
        return msg

    def listen(self, guid: str):
        q = queue.Queue(maxsize=2)
        self.listeners[guid].append(q)
        return q

    def announce(self, msg, guid: str):
        data = self.__format_sse(msg)
        for i in reversed(range(len(self.listeners[guid]))):
            try:
                self.listeners[guid][i].put_nowait(data)
            except queue.Full:
                del self.listeners[guid][i]

    def assign_role_api(self):
        session = self.sessions_roles[-1]
        if 'navigator' not in session:
            guid = str(uuid.uuid4())
            session['navigator'] = guid
            self.sessions_resp[guid] = {}
            return 'navigator', guid
        elif 'instructor' not in session:
            self.sessions_roles.append({})
            return 'instructor', session['navigator']

    def upload(self, data):
        guid = data['guid']
        role = data['game_config']['game_role']
        self.sessions_resp[guid][role] = data
        if len(self.sessions_resp[guid]) == 1:
            return None
        else:
            combined_data = {}
            navigator_data = self.sessions_resp[guid][0]
            instructor_data = self.sessions_resp[guid][1]

            combined_data['guid'] = guid
            combined_data['game_config'] = {'game_mode': 'human'}

            combined_data['chat'] = navigator_data['chat']
            combined_data['navigator_metadata'] = navigator_data['user_metadata']
            combined_data['navigator_survey'] = navigator_data['user_survey']
            combined_data['user_map_path'] = navigator_data['user_map_path']

            combined_data['instructor_metadata'] = instructor_data['user_metadata']
            combined_data['instructor_survey'] = instructor_data['user_survey']

            del self.sessions_resp[guid]
            return combined_data
