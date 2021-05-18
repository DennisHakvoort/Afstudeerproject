import logging
from datetime import datetime
from time import time
from typing import List

from data_loader.loaders.Loader import Loader
from helper.ConfigReader import get_string_property
from helper.paths import get_root_dir
from models.UnprocessedDocument import UnprocessedDocument


# BBC stands for British Broadcasting Corporation, the news site our dataset is from.
class BBCLoader(Loader):
    LOG: logging.Logger = None
    _bbc_path = None

    def __init__(self):
        self.LOG = logging.getLogger(__name__)
        self._bbc_path = get_root_dir() / get_string_property("path", "BBC_documents")

    def retrieve_documents(self, since: datetime) -> List[UnprocessedDocument]:
        if not self._bbc_path.is_dir():
            self.LOG.critical("The BBC file directory does not exist. Please see the manual for instructions")
            raise FileNotFoundError("The BBC file directory does not exist. Please see the manual for instructions")

        self.LOG.debug("Beginning BBC data loading...")
        start_time = time()
        fetched_documents: List[UnprocessedDocument] = []
        categories: List[str] = ["business", "entertainment", "politics", "sport", "tech"]
        start_index = 1
        # Because the BBC dataset uses the same id's within each category, we append a number corresponding to the
        # current category index in front of the id as a 3 number string, this makes all id's unique.
        for i, category in enumerate(categories, start_index):
            for j, text in enumerate(self._get_category_documents(category)):
                split_body = text.splitlines()
                title = split_body[0]  # The title is always the first line of the document, the rest is body
                body = " ".join(split_body[1:])
                fetched_documents.append(UnprocessedDocument(
                    document_id=str(i) + "{0:0=3d}".format(j),
                    body_raw=body,
                    title_raw=title,
                    space="BBC"
                ))
        self.LOG.info("Finished BBC data loading in %0.3fs" % (time() - start_time))
        return fetched_documents

    def _get_category_documents(self, category: str) -> List[str]:
        fetched_documents: List[str] = []
        dir_path = self._bbc_path / "{}".format(category)
        for file in dir_path.glob("*.txt"):
            self.LOG.debug("File {} has been loaded.".format(str(file)))
            with open(file, encoding="latin-1") as document:
                fetched_documents.append(document.read())
        return (fetched_documents)
