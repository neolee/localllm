from openai import OpenAI

import json


# init client point to the local server, api_key is irrelevant
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# model_name = "NousResearch/Hermes-3-Llama-3.1-8B-GGUF/Hermes-3-Llama-3.1-8B.Q8_0.gguf"
# model_name = "bartowski/Qwen2.5-32B-Instruct-GGUF/Qwen2.5-32B-Instruct-IQ4_XS.gguf"
# model_name = "bartowski/Qwen2.5-Coder-32B-Instruct-GGUF/Qwen2.5-Coder-32B-Instruct-IQ4_XS.gguf"
model_name = "lmstudio-community/Qwen2.5-Coder-32B-Instruct-MLX-4bit"

system_message_file = "system_message.txt"

user_name = "Neo"
agent_name = "Garfield"

def load_system_message():
    newline = '\n'
    with open(system_message_file, 'r') as f:
        system_message = f"{f.read().replace(newline, ' ')}".format(**globals())
    return system_message

def simple_chat_completion(q, sm):
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": sm},
            {"role": "user", "content": q}
        ],
        temperature=0.7
    )

def chat_completion(stream, history):
    return client.chat.completions.create(
        model=model_name,
        messages=history, # type: ignore
        temperature=0.7,
        stream=stream
    )

def stringify_history(history):
    s = f"\n{'-'*20} History dump {'-'*20}\n"
    s += json.dumps(history, indent=2)
    s += f"\n{'-'*55}"
    return s
