from openai import OpenAI

from bot import Bot


# init client point to the local server, api_key is irrelevant
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model_name = "NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF"

system_message_file = "system_message.txt"

user_name = "Neo"
agent_name = "Garfield"

def load_system_message():
    newline = '\n'
    with open(system_message_file, 'r') as f:
        system_message = f"{f.read().replace(newline, ' ')}".format(**globals())
    return system_message

def create_chat_completion(q, sm):
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": sm},
            {"role": "user", "content": q}
        ],
        temperature=0.7,
    )


class LLMBot(Bot):
    def __init__(self, runtype='looped'):
        super().__init__(runtype)
        self.q = "I'm now backed by the newest LLM. Let's talk."
        self.system_message = load_system_message()

    def _think(self, s):
        completion = create_chat_completion(s, self.system_message)
        return completion.choices[0].message.content
