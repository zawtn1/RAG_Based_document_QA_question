from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
DATA_PATH = BASE_DIR / "data/documents"
VECTOR_DB_PATH = BASE_DIR / "vector_store"