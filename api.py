from openai import OpenAI


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

def simple_chat_completion(q, sm):
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": sm},
            {"role": "user", "content": q}
        ],
        temperature=0.7
    )

def stream_chat_completion(history):
    return client.chat.completions.create(
        model=model_name,
        messages=history, # type: ignore
        temperature=0.7,
        stream=True
    )
