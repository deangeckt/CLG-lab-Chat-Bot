from time import sleep


class Bot:
    def __init__(self):
        print('Init Bot')
        self.chat = []
        self.mock_resp = ["Keep going left towards the parrot",
                          "Bypass the parrot from above",
                          "Go between the parrot and the elephant"]
        self.resp_idx = 0

    def __get_next(self):
        if self.resp_idx == len(self.mock_resp):
            return 'finish'
        res = self.mock_resp[self.resp_idx]
        self.resp_idx += 1
        return res

    def call(self, user_msg):
        print(f'Bot call with: {user_msg}')
        sleep(2)
        self.chat.append(user_msg)  # keep history
        return self.__get_next()
