import logging
from pathlib import Path

from .base import BASE_DIR

LOGGING_TOTAL_PATH = Path(BASE_DIR, 'logs', 'total.log')


formatter = logging.Formatter(fmt='%(message)s')

file_log = logging.FileHandler(filename=LOGGING_TOTAL_PATH)
console_out = logging.StreamHandler()

handlers = (
    file_log,
    console_out,
)

console_out.setFormatter(fmt=formatter)
file_log.setFormatter(fmt=formatter)

logging.basicConfig(handlers=handlers, level=logging.DEBUG)
