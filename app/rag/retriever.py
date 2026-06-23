from langchain_community.vectorstores import FAISS

from app.core.config import VECTOR_DB_PATH
from app.rag.embeddings import get_embeddings


def get_retriever(user_id):
    user_vector_path = VECTOR_DB_PATH / f"user_{user_id}"
    index_file = user_vector_path / "index.faiss"
    if not index_file.exists():
        return None

    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        str(user_vector_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore.as_retriever()
