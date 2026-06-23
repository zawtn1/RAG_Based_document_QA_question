import argparse
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import DATA_PATH, VECTOR_DB_PATH
from app.rag.embeddings import get_embeddings


def ingest_documents(user_id):
    user_data_path = DATA_PATH / f"user_{user_id}"
    user_vector_path = VECTOR_DB_PATH / f"user_{user_id}"
    user_data_path.mkdir(parents=True, exist_ok=True)

    documents = []
    for file in user_data_path.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())

    if not documents:
        # No PDFs left for this user (e.g. last one was deleted) - drop any
        # stale index so the retriever doesn't keep serving old data.
        if user_vector_path.exists():
            shutil.rmtree(user_vector_path)
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    user_vector_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(user_vector_path))

    print(f"Indexed {len(documents)} document(s) for user {user_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manually (re)index a user's documents")
    parser.add_argument("--user-id", type=int, required=True)
    args = parser.parse_args()
    ingest_documents(args.user_id)
