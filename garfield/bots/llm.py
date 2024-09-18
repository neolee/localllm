from garfield.bot import Bot
from api import load_system_message
from api import simple_chat_completion, stream_chat_completion
from api import stringify_history


class SimpleLLMBot(Bot):
    def __init__(self, runtype='looped'):
        super().__init__(runtype)
        self.q = "I'm now backed by the newest LLM. Let's talk."
        self.system_message = load_system_message()

    def _think(self, s):
        completion = simple_chat_completion(s, self.system_message)
        return completion.choices[0].message.content


class LLMBot(Bot):
    def __init__(self, runtype='custom', verbose=False):
        super().__init__(runtype)
        self.verbose = verbose
        self.welcome_message = "Hello, introduce yourself to someone opening this program for the first time. Be concise."
        self.system_message = load_system_message()
        self.history = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.welcome_message},
        ]

    def _show_history(self):
        self._print(stringify_history(self.history), 'light_grey')

    def _preprocessing(self, q):
        return q

    def run(self):
        while True:
            completion = stream_chat_completion(self.history)

            new_message = {"role": "assistant", "content": ""}

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(self._format(chunk.choices[0].delta.content), end="", flush=True)
                    new_message["content"] += chunk.choices[0].delta.content

            self.history.append(new_message)

            if self.verbose: self._show_history()
            else: print()

            print()
            q = input("> ")
            if q.lower() in ['q', 'x', 'quit', 'exit', 'bye']: break
            context = self._preprocessing(q)
            self.history.append({"role": "user", "content": context})
