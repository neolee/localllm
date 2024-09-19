from time import sleep
from termcolor import colored, cprint


class Bot:
    EXIT_NORMAL = 0
    EXIT_RESTART = 1

    wait = 1

    # self.runtype: run type of the bot, can be 'once' or 'looped', default to 'once'
    def __init__(self, runtype='once'):
        self.runtype = runtype
        self.q = ''

    def _think(self, s):
        return s

    def _format(self, s, c='blue'):
        return colored(s, c) # type: ignore

    def _print(self, s, c='blue'):
        cprint(s, c) # type: ignore

    def _say(self, s):
        sleep(Bot.wait)
        self._print(s)

    def _is_command_quit(self, s):
        return s.lower() in [':q', ':x', ':quit', ':exit', 'bye']

    def _is_command_restart(self, s):
        return s.lower() in [':r', ':restart', ':reset']

    def _run_once(self):
        self._say(self.q)
        q = input()
        self._say(self._think(q))
        return Bot.EXIT_NORMAL

    def _run_looped(self):
        self._say(self.q)
        while True:
            q = input()
            if self._is_command_quit(q): return Bot.EXIT_NORMAL
            if self._is_command_restart(q): return Bot.EXIT_RESTART
            self._say(self._think(q))

    def run(self):
        match self.runtype:
            case 'once': return self._run_once()
            case 'looped': return self._run_looped()
            case _: return Bot.EXIT_NORMAL
