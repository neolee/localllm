from garfield.bot import Bot
from api import load_system_message
from api import simple_chat_completion, chat_completion
from api import stringify_history

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "true"


class SimpleLLMBot(Bot):
    def __init__(self, runtype='looped'):
        super().__init__(runtype)
        self.q = "I'm now backed by the newest LLM. Let's talk."
        self.system_message = load_system_message()

    def _think(self, s):
        completion = simple_chat_completion(s, self.system_message)
        return completion.choices[0].message.content


class LLMBot(Bot):
    def __init__(self, runtype='custom', stream=True, verbose=False):
        super().__init__(runtype)
        self.stream = stream
        self.verbose = verbose
        self.welcome_message = "Introduce yourself to someone opening this program for the first time. Be concise."
        self.system_message = load_system_message()
        self.history = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.welcome_message},
        ]

    def _show_history(self):
        self._print(stringify_history(self.history), 'light_grey')

    # called after completion return from the model
    def _postprocessing(self, content):
        return content

    # called before provide context to the model
    def _preprocessing(self, q):
        return q

    def run(self):
        while True:
            new_message = {"role": "assistant", "content": ""}
            completion = chat_completion(self.stream, self.history)
            if self.stream:
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        print(self._format(chunk.choices[0].delta.content), end="", flush=True)
                        new_message["content"] += chunk.choices[0].delta.content
                print()
            else:
                response = self._postprocessing(completion.choices[0].message.content)
                self._print(response)
                new_message["content"] = response

            self.history.append(new_message)

            # print history if in verbose mode
            if self.verbose: self._show_history()
            else: print()

            q = input("> ")
            if self._is_command_quit(q): return Bot.EXIT_NORMAL
            if self._is_command_restart(q): return Bot.EXIT_RESTART
            context = self._preprocessing(q)
            self.history.append({"role": "user", "content": context})
