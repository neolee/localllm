from time import sleep
from termcolor import colored


class Bot:
    wait = 1

    # self.runtype: run type of the bot, can be 'once' or 'looped', default to 'once'
    def __init__(self, runtype='once'):
        self.runtype = runtype
        self.q = ''
        self.a = ''

    def _think(self, s):
        return s

    @staticmethod
    def _format(s):
        return colored(s, 'blue')

    def _say(self, s):
        sleep(Bot.wait)
        print(self._format(s))

    def _run_once(self):
        self._say(self.q)
        self.a = input()
        self._say(self._think(self.a))

    def _run_looped(self):
        self._say(self.q)
        while True:
            self.a = input()
            if self.a.lower() in ['q', 'x', 'quit', 'exit', 'bye']:
                break
            self._say(self._think(self.a))

    def run(self):
        if self.runtype == 'once':
            self._run_once()
        elif self.runtype == 'looped':
            self._run_looped()
