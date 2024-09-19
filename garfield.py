from garfield.bots.builtin import *
from garfield.bots.llm import SimpleLLMBot, LLMBot
from garfield.bots.rag import RAGBot
from garfield.bots.cot import CoTBot


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

    def _menu_select(self):
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
        return bot_index - 1

    def _run_list_mode(self):
        while True:
            bot_index = self._menu_select()
            bot = self.bots[bot_index]
            print()
            match bot.run():
                case Bot.EXIT_RESTART: continue
                case _: break


if __name__ == '__main__':
    garfield = Garfield(1, 'list')
    garfield.add(HelloBot())
    garfield.add(GreetingBot())
    garfield.add(FavoriteColorBot())
    garfield.add(CalcBot('looped'))
    garfield.add(SimpleLLMBot('looped'))
    garfield.add(LLMBot())
    garfield.add(RAGBot())
    garfield.add(CoTBot())
    garfield.run()
