import queue
import uuid
from collections import defaultdict


class Server:
    def __init__(self):
        self.sessions = [{}]
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
        session = self.sessions[-1]
        if 'navigator' not in session:
            guid = str(uuid.uuid4())
            session['navigator'] = guid
            return 'navigator', guid
        elif 'instructor' not in session:
            self.sessions.append({})
            return 'instructor', session['navigator']

