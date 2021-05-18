import logging
from datetime import datetime
from typing import List

from data_loader.loaders.BBCLoader import BBCLoader
from data_loader.loaders.ConfluenceLoader import ConfluenceLoader
from data_loader.loaders.Loader import Loader
from helper.ConfigReader import get_string_property
from helper.Singleton import Singleton
from models.UnprocessedDocument import UnprocessedDocument


class DataLoader(metaclass=Singleton):
    LOG = logging.getLogger(__name__)
    loader: Loader = None

    def __init__(self):
        datasource_switcher = {
            "CONFLUENCE": self._init_confluence_loader,
            "BBC": self._init_bbc_loader
        }

        datasource = get_string_property('datasource', 'data_source')
        datasource_switcher.get(datasource, self._init_default)()
        self.LOG.info("the DataLoader has been created for the datasource: {}".format(datasource))

    def retrieve_documents(self, since: datetime) -> List[UnprocessedDocument]:
        return self.loader.retrieve_documents(since)

    def _init_confluence_loader(self):
        self.loader = ConfluenceLoader()

    def _init_bbc_loader(self):
        self.loader = BBCLoader()

    def _init_default(self):
        raise ValueError(
            "The datasource {} is invalid. Please consult the manual for possible loaders.".format(
                get_string_property('datasource', 'data_source')))
