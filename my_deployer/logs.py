"""Logging-related utility functions.

Provide a friendly interface to log the deployer's operations.
"""
import logging


LOG_FORMAT = "%(asctime)s - [%(levelname)8s] - %(name)s: %(message)s"


def build_logger(name: str) -> logging.Logger:
    """Configure a logger with a `name`.

    Example output:
        2020-10-30 17:55:59,927 - [    INFO ] - SSHOperator: executed and got result = 0
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
