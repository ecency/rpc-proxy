import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'log'))
log_path = os.path.join(log_dir, 'rpc-proxy.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def create_logger(name, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')

    # file logger
    handler_file = RotatingFileHandler(log_path, maxBytes=1024 * 100000, backupCount=10)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)

    return logger
