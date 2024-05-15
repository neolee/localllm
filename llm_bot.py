from bot import Bot
from api import load_system_message, simple_chat_completion, stream_chat_completion


class LLMBot(Bot):
    def __init__(self, runtype='looped'):
        super().__init__(runtype)
        self.q = "I'm now backed by the newest LLM. Let's talk."
        self.system_message = load_system_message()

    def _think(self, s):
        completion = simple_chat_completion(s, self.system_message)
        return completion.choices[0].message.content


class StreamLLMBot(Bot):
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
        import json
        gray_color = "\033[90m"
        reset_color = "\033[0m"
        print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        print(json.dumps(self.history, indent=2))
        print(f"\n{'-'*55}\n{reset_color}")

    def run(self):
        while True:
            completion = stream_chat_completion(self.history)

            new_message = {"role": "assistant", "content": ""}

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    new_message["content"] += chunk.choices[0].delta.content

            self.history.append(new_message)

            if self.verbose: self._show_history()

            print('\n')
            q = input("> ")
            if q.lower() in ['q', 'x', 'quit', 'exit', 'bye']: break
            self.history.append({"role": "user", "content": q})
            print()
