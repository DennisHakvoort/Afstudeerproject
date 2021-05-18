from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from models.UnprocessedDocument import UnprocessedDocument


# This class contains the methods for the other datasource loaders.

class Loader(ABC):

    @abstractmethod
    def retrieve_documents(self, since: datetime) -> List[UnprocessedDocument]:
        raise ValueError("Please don't call {} directly, use one of its implementations instead.".format(__name__))
