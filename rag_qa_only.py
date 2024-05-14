from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.utils.utils import convert_to_secret_str

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# query the chroma vector db for similar
embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

query = "What is the CAP theorem?"

print("\nSearching for similar documents to:", query, "\n")

# search and show the result
search_results = vector_db.similarity_search(query, k=2)
search_results_string = ""
for result in search_results:
    search_results_string += result.page_content + "\n"
print(search_results_string)

# feed to llm
llm = ChatOpenAI(temperature=0.5,
                 base_url="http://localhost:1234/v1",
                 api_key=convert_to_secret_str("lm-studio"))

# build prompt
template = """Use the following pieces of context to answer the question at the end. \
    If you don't know the answer, just say that you don't know, don't try to make up an answer. \
    Use three sentences maximum. {context} \
    Question: {question}
    Helpful Answer:"""
qa_chain_prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# run chain
question = "What is the CAP theorem?"
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vector_db.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": qa_chain_prompt})

print("Running AI...\n")
result = qa_chain.invoke({"query": question})
print(result["result"])
