import configparser
import logging
import sys

from helper.paths import get_root_dir

# This file contains some functions that can be used to read data from the config file. The usage of this file gives
# some benifits such as one static definition for the config file location and error reporting.

config_file = None
LOG = logging.getLogger(__name__)


def _read_property(section: str, option: str) -> str:
    global config_file
    if config_file is None:
        config_file = _load_config()
    returnable = config_file.get(section, option)
    logging.getLogger(__name__).debug(
        "The config was queried with [{}]: {}, returning {}.".format(section, option, returnable))
    return returnable


def _load_config() -> configparser.ConfigParser:
    configfile = get_root_dir().joinpath("config", "config.ini")
    config = configparser.RawConfigParser()
    if configfile.is_file():
        config.read(configfile)
        return config
    else:
        error_message = "The config file {} was not found. Please check the documentation and create the config file." \
            .format(str(configfile))
        LOG.critical(error_message)
        sys.exit(error_message)


def get_string_property(section: str, option: str) -> str:
    return _read_property(section, option)


def get_bool_property(section: str, option: str) -> bool:
    return _read_property(section, option).lower() == "true"


def get_int_property(section: str, option: str) -> int:
    return int(_read_property(section, option))
