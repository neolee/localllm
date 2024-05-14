from random import choice
from simpleeval import simple_eval, InvalidExpression

from bot import Bot


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
