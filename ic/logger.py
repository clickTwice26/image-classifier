import os
import logging
import datetime as dt
from logging.handlers import RotatingFileHandler

LOG_FOLDER_NAME = "logs"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s - %(funcName)s - %(lineno)d - %(pathname)s"
DEFAULT_LOG_OUT_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

if not os.path.exists(LOG_FOLDER_NAME):
    os.makedirs(LOG_FOLDER_NAME)

today = dt.date.today()
logFileName = f"{LOG_FOLDER_NAME}/{today.month:02d}-{today.day:02d}-{today.year}.log"

def setup_logger():
    logger = logging.getLogger("flaskAppLogger")
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(logFileName, maxBytes=1000000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
