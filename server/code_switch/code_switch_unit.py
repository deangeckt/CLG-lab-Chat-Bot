
class CodeSwitchUnit:
    def __init__(self):
        pass

    def call(self, user_msg: str, en_bot_resp: list[str]):
        """
        param user_msg: last user chat message in spanglish
        param en_bot_resp: the generated messages (list) the bot generated in english
        :return: spanglish generated string in a list
        """
        return en_bot_resp

