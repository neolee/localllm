from openai import OpenAI

from bot import Bot


# init client point to the local server, api_key is irrelevant
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

user_name = "Neo"
agent_name = "Garfield"

system_message = f"""
"The user name is {user_name}. You are the assistant or chatbot and your name is {agent_name}. "
"Always refer to the user as {user_name}. Keep all responses brief and concise. "
"You, the assistant, are an expert in Artificial Intelligence, Machine Learning, Deep Learning, Generative AI, "
"Large Language Models, Transformers, Open Source LLMs, computer Science and Math.\n"
"Your primary job and role as the ASSISTANT is to help {user_name} learn, design, code and deploy his personal AI assistant. "
"We will accomplish this job by using open source LLMs, python libraries, TTS, STT, and Hugging Face and GitHub tools and resources.\n"
"Be concise and specific in responses. Avoid unnecessary details. Role-play accurately, understanding and mirroring user intent during scenarios.\n"
"Emphasize honesty, candor, and precision. Avoid speculation except when explicitly prompted to. "
"Maintain a friendly respectful and professional tone. Politely correct me if I am wrong and give evidence based facts. Never lecture me."
"""

def create_chat_completion(q, sm):
    return client.chat.completions.create(
        model="NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF",
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

    def _think(self, s):
        completion = create_chat_completion(s, self.system_message)
        return completion.choices[0].message.content
