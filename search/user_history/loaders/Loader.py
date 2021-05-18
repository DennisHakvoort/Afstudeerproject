from abc import ABC, abstractmethod
from typing import List


# This class contains the methods for the other datasource loaders.

class Loader(ABC):

    @abstractmethod
    def retrieve_history(self, username: str) -> List[str]:
        raise ValueError("Please don't call {} directly, use one of its implementations instead.".format(__name__))
