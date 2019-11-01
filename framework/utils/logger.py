import logging
import logging.config

from resources import config

logging.basicConfig(level=config.LOGGING_LEVEL, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


def info(message: str):
    logging.info(message)


def warning(message: str):
    logging.warning(message)


def error(message: str):
    logging.error(message)


def debug(message: str):
    logging.debug(message)


class Step:
    steps_counter: int = 1

    def __init__(self, message: str):
        self.message = message

    def __enter__(self):
        logging.info(f"<<<Step {Step.steps_counter}>>>: {self.message}")
        return self

    def __exit__(self, type, value, traceback):
        Step.steps_counter += 1
        return isinstance(value, TypeError)
