import logging
import sys

import psycopg2

from helper.ConfigReader import get_string_property

LOG = logging.getLogger(__name__)


def connect_to_database():
    '''
    Connects to the postgresql database, and returns the connection.
    '''
    try:
        return psycopg2.connect(user=get_string_property("database", "user"),
                                password=get_string_property("database", "password"),
                                host=get_string_property("database", "host"),
                                port=get_string_property("database", "port"),
                                database=get_string_property("database", "database"))

    except psycopg2.Error as error:
        error_message = "Could not connect to the database, the following error was thrown: {}".format(error)
        LOG.critical(error_message)
        sys.exit(error_message)
