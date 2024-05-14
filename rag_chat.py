from openai import OpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

import json


def show_history(history):
    gray_color = "\033[90m"
    reset_color = "\033[0m"
    print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    print(json.dumps(history, indent=2))
    print(f"\n{'-'*55}\n{reset_color}")


def main():
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."}
    ]

    while True:
        completion = client.chat.completions.create(
            model="local-model",
            messages=history, # type: ignore
            temperature=0.7,
            stream=True
        )

        message = {"role": "assistant", "content": ""}
        for chunk in completion:
            s = chunk.choices[0].delta.content
            if s:
                print(s, end="", flush=True)
                message["content"] += s

        history.append(message)

        # uncomment following to see chat history
        # show_history(history)

        print('\n')

        q = input("> ")
        if q.lower() in ['q', 'x', 'quit', 'exit', 'bye']: break
        search_results = vector_db.similarity_search(q, k=2)
        context = ""
        for result in search_results:
            context += result.page_content + "\n\n"
        history.append({"role": "user", "content": context + q})
        print()


if __name__ == "__main__":
    main()
