import queue


# TODO: should be Q for a game id / session

class Server:
    def __init__(self):
        self.session = {}
        # self.curr_session = 0
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
        # session = self.sessions[self.curr_session]
        if '0' not in self.session:
            self.session['0'] = '0'
            return 0
        elif '1' not in self.session:
            self.session = {}
            return 1

