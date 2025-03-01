from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).parent.parent.absolute()

LOGGING_CONFIG_PATH = PROJECT_ROOT_DIR / "logging.ini"

EXTERNAL_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "external"
RAW_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "raw"
PROCESSED_DATA_FOLDER = PROJECT_ROOT_DIR / "data" / "processed"
TRAIN_DATA_FOLDER = PROCESSED_DATA_FOLDER / "train"
TEST_DATA_FOLDER = PROCESSED_DATA_FOLDER / "test"
MODELS_FOLDER = PROJECT_ROOT_DIR / "models"


RSS_FEEDS = [
    "https://www.computerworld.com/index.rss",
    "https://www.wired.com/feed/rss",
    "https://rss.slashdot.org/Slashdot/slashdot",
    "https://www.theverge.com/rss/index.xml",
]

FETCH_PERIOD_HOURS = 6

LOG_PERIOD = 100
TEST_TRAIN_RATIO = 0.9
