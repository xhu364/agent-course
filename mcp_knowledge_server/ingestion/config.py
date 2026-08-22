from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_FILE = BASE_DIR / "data" / "documents" / "company_policy.txt"
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 2000
OVERLAP = 150
SIMILARITY_THRESHOLD = 0.75