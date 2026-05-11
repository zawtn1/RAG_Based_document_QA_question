from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.core.config import DATA_PATH, VECTOR_DB_PATH


def ingest_documents():

    documents = []

    for file in DATA_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(str(VECTOR_DB_PATH))

    print("Documents indexed successfully!")


if __name__ == "__main__":
    ingest_documents()