import queue


class Server:
    def __init__(self):
        self.session = {}
        self.listeners = []

    @staticmethod
    def __format_sse(data: str):
        msg = f'data: {data}\n\n'
        return msg

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        data = self.__format_sse(msg)
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(data)
            except queue.Full:
                del self.listeners[i]

    def assign_role_api(self):
        if 'navigator' not in self.session:
            self.session['navigator'] = ''
            return 'navigator'
        elif 'instructor' not in self.session:
            self.session = {}
            return 'instructor'
