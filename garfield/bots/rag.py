from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from garfield.bots.llm import LLMBot


class RAGBot(LLMBot):
    def __init__(self, runtype='custom', stream=True, verbose=False):
        super().__init__(runtype, stream, verbose)
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db = Chroma(persist_directory="./chroma_db",
                                embedding_function=self.embedding_function)

    def _preprocessing(self, q):
        search_results = self.vector_db.similarity_search(q, k=2)
        context = ""
        for result in search_results:
            context += result.page_content + "\n\n"
        return context
