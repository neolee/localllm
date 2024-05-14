from random import choice
from time import sleep
from termcolor import colored
from simpleeval import simple_eval, InvalidExpression


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
            if self.a.lower() in ['q', 'x', 'quit', 'exit']:
                break
            self._say(self._think(self.a))

    def run(self):
        if self.runtype == 'once':
            self._run_once()
        elif self.runtype == 'looped':
            self._run_looped()


class HelloBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "Hi, what is your name?"

    def _think(self, s):
        return f"Hello {s}"


class GreetingBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "How are you today?"

    def _think(self, s):
        if 'good' in s.lower() or 'fine' in s.lower():
            return "I'm feeling good too"
        else:
            return "Sorry to hear that"


class FavoriteColorBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "What's your favorite color?"

    def _think(self, s):
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']
        return f"You like {s.lower()}? My favorite color is {choice(colors)}"


class CalcBot(Bot):
    def __init__(self, runtype='once'):
        super().__init__(runtype)
        self.q = "Through recent upgrade I can do calculation now. Input some arithmetic expression to try, " \
                 "input 'q' 'x' 'quit' or 'exit' to quit:"

    def _think(self, s):
        try:
            result = f"Done. Result = {simple_eval(s)}"
        except InvalidExpression:
            result = "Sorry I can't understand"

        return result


class Garfield:
    def __init__(self, wait=1, mode='default'):
        Bot.wait = wait
        self.bots = []
        self.mode = mode

    def add(self, bot):
        self.bots.append(bot)

    @staticmethod
    def _prompt(s):
        print(s)
        print()

    def run(self):
        self._prompt("This is Garfield dialog system. Let's talk.")

        if self.mode == 'list':
            self._run_list_mode()
        else:
            self._run_default_mode()

    def _run_default_mode(self):
        for bot in self.bots:
            bot.run()

    def _run_list_mode(self):
        for index, bot in enumerate(self.bots):
            print(f"{index + 1}. {type(bot).__name__}")

        bot_index = 0
        bot_count = len(self.bots)
        input_prompt = f"Enter a number to choose your friend (1-{bot_count}): "
        while True:
            try:
                bot_index = int(input(input_prompt))
            except ValueError:
                print(f"Not a valid number. Please retry.")
                continue

            if bot_index < 1 or bot_index > bot_count:
                print(f"You can only choose between 1-{bot_count}")
                continue
            else:
                break

        bot = self.bots[bot_index - 1]
        bot.run()


if __name__ == '__main__':
    garfield = Garfield(1, 'list')
    garfield.add(HelloBot())
    garfield.add(GreetingBot())
    garfield.add(FavoriteColorBot())
    garfield.add(CalcBot('looped'))
    garfield.run()
