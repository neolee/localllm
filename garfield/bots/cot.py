import re
from txtai import Embeddings

from garfield.bots.llm import LLMBot


class CoTBot(LLMBot):
    def __init__(self, runtype="custom", stream=False, verbose=False):
        super().__init__(runtype, stream, verbose)

        # init the embedding wikipedia vector data
        self.embeddings = Embeddings()
        self.embeddings.load(provider="huggingface-hub", container="neuml/txtai-wikipedia")

        # the chain-of-thought prompt courtesy of
        # https://github.com/codelion/optillm/blob/main/cot_reflection.py
        self.system_message = f"""
        {self.system_message}

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

    def _postprocessing(self, content):
        # extract and return `output` part
        if content:
            match = re.search(r"<output>(.*?)(?:</output>|$)", content, re.DOTALL)
            return match.group(1).strip() if match else content
        else: return ""

    def _preprocessing(self, q):
        if not self.embeddings: return q

        context = "\n".join([x["text"] for x in self.embeddings.search(q)]) # type: ignore
        prompt = f"""
        Answer the following question using only the context below. Only include information
        specifically discussed.

        question: {q}
        context: {context}
        """

        return prompt
