import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from contextvars import ContextVar

correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="system")

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True
    
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        log_file = os.path.join(LOG_DIR, "archie.log")
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
        json_formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s')
        file_handler.setFormatter(json_formatter)
        console_handler = logging.StreamHandler(sys.stdout)
        pretty_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(correlation_id)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(pretty_formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.addFilter(CorrelationIdFilter())
        logger.setLevel(logging.INFO)
    return logger

log = get_logger("archie-ai")