from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LANCEDB_DIR = BASE_DIR / "lancedb"
VECTOR_DB_PATH = LANCEDB_DIR 