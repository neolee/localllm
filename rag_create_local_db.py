# create a vector database from a pdf file

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


# load pdf text
pdfs = ['./books/cap.pdf',
        './books/feynman-cn.pdf',
        './books/illiberal-democracy.pdf',
        './books/mysterious-cases-cn.pdf',
        './books/sicp.pdf']
docs = []
for file in pdfs:
    print('loading', file)
    loader = PyPDFLoader(file)
    docs.extend(loader.load())

# split text to chunks
print('splitting text to chunks')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# load it into chroma
print('writing into chroma db')
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")
print('done')
