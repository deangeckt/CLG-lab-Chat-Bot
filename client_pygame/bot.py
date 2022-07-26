import queue
from time import sleep
from threading import Thread

q = queue.Queue()


class Bot:
    def __init__(self, chat):
        self.chat = chat
        self.t = Thread(target=self.task)
        self.t.daemon = True
        self.t.start()
        self.first_msg_sent = False

        self.resp = ["Keep going left towards the parrot",
                     "Bypass the parrot from above",
                     "Go between the parrot and the elephant"]
        self.resp_idx = 0

    def get_next(self):
        if self.resp_idx == len(self.resp):
            return 'finish'
        res = self.resp[self.resp_idx]
        self.resp_idx += 1
        return res

    def task(self):
        while True:
            sleep(5)
            if not self.first_msg_sent:
                self.chat.add_text("hello, start by going left towards the tiger", 'bot')
                self.first_msg_sent = True

            print("sampling Q")
            try:
                obj = q.get()
                print(obj)
                if obj['speaker'] == 'user':
                    self.chat.add_text(self.get_next(), 'bot')
            except:
                pass