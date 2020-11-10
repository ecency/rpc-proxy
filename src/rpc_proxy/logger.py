import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

log_path = os.path.join(str(Path.home()), 'rpc-proxy.log')


def create_logger(name, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')

    # file logger
    handler_file = RotatingFileHandler(log_path, maxBytes=1024 * 100000, backupCount=10)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)

    return logger
