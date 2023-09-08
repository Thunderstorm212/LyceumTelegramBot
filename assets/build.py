from lib import Colors
from assets.bot import Bot
from assets.admin import Admin


class Build(Bot, Admin):
    def __init__(self):
        super(Build, self).__init__()

    @staticmethod
    def status(inp: bool):
        if inp:
            print(Colors("✅| Build done |", "#6a994e"))







