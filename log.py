import logging
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / 'log' / 'jobboard.log'
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)

def setup_logger(app):
    app.logger.handlers.clear()
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = True