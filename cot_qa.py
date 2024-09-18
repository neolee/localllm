import re
from txtai import Embeddings
from api import simple_chat_completion


import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "true"
# and keep `transformers~=4.43.*` to prevent the `clean_up_tokenization_spaces` warning


# prompt courtesy of  https://github.com/codelion/optillm/blob/main/cot_reflection.py
def cot(system_prompt, user_prompt):
    system_prompt = f"""
    {system_prompt}

    You are an AI assistant that uses a Chain of Thought (CoT) approach with reflection to answer queries. Follow these steps:

    1. Think through the problem step by step within the <thinking> tags.
    2. Reflect on your thinking to check for any errors or improvements within the <reflection> tags.
    3. Make any necessary adjustments based on your reflection.
    4. Provide your final, concise answer within the <output> tags.

    Important: The <thinking> and <reflection> sections are for your internal reasoning process only.
    Do not include any part of the final answer in these sections.
    The actual response to the query must be entirely contained within the <output> tags.

    Use the following format for your response:
    <thinking>
    [Your step-by-step reasoning goes here. This is your internal thought process, not the final answer.]
    <reflection>
    [Your reflection on your reasoning, checking for errors or improvements]
    </reflection>
    [Any adjustments to your thinking based on your reflection]
    </thinking>
    <output>
    [Your final, concise answer to the query. This is the only part that will be shown to the user.]
    </output>
    """

    completion = simple_chat_completion(user_prompt, system_prompt)
    response = completion.choices[0].message.content

    # extract and return output
    if response:
        match = re.search(r"<output>(.*?)(?:</output>|$)", response, re.DOTALL)
        return match.group(1).strip() if match else response
    else: return ""

def rag(embeddings, question):
    prompt = """
    Answer the following question using only the context below. Only include information
    specifically discussed.

    question: {question}
    context: {context}
    """

    system_prompt = "You are a friendly assistant. You answer questions from users."

    context = "\n".join([x["text"] for x in embeddings.search(question)])

    return cot(system_prompt, prompt.format(question=question, context=context))

# wikipedia embeddings index
embeddings = Embeddings()
embeddings.load(provider="huggingface-hub", container="neuml/txtai-wikipedia")

# rag + cot with self-reflection
print(rag(embeddings, "Tell me about how jet engines work"))
print(rag(embeddings, "What is illiberal democracy?"))
