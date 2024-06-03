from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from api import stream_chat_completion, stringify_history


def show_history(history):
    print(stringify_history(history))


def main():
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."}
    ]

    while True:
        completion = stream_chat_completion(history)

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
