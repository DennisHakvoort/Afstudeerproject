import logging

from delegator.delegator import start_data_loading
from helper.ConfigReader import get_string_property


def _setup_logger():
    logformat = get_string_property("logging", "format")
    loglevel = logging.getLevelName(get_string_property("logging", "level"))
    logging.basicConfig(format=logformat, level=loglevel)
    logging.info("Logger initiated")

if __name__ == '__main__':
    _setup_logger()

    start_data_loading()
