from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.utils.utils import convert_to_secret_str
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# query the chroma vector db for similar
embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

query = "What is the CAP theorem?"

print("> searching for similar documents to:", query, "\n")

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
system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# build chain
retriever = vector_db.as_retriever()
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

# run chain
question = query
print("> running lang chain and ask:", question, "\n")
result = chain.invoke({"input": question})
print(result['answer'])
