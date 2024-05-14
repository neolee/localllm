from bot import Bot
from api import load_system_message, create_chat_completion


class LLMBot(Bot):
    def __init__(self, runtype='looped'):
        super().__init__(runtype)
        self.q = "I'm now backed by the newest LLM. Let's talk."
        self.system_message = load_system_message()

    def _think(self, s):
        completion = create_chat_completion(s, self.system_message)
        return completion.choices[0].message.content
