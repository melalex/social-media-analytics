from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).parent.parent.absolute()

LOGGING_CONFIG_PATH = PROJECT_ROOT_DIR / "logging.ini"

EXTERNAL_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "external"
RAW_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "raw"
PROCESSED_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "processed"

NEO4J_URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"
