import logging
from typing import List

from user_history.loaders.Loader import Loader


# BBC stands for British Broadcasting Corporation, the news site our dataset is from.
class BBCLoader(Loader):
    LOG = logging.getLogger(__name__)

    def retrieve_history(self, username: str) -> List[str]:
        # Our BBC dataset really doesn't have anything representing a user history.
        # However, because it's frequently used for testing and debugging, this file is
        # included. We just return a list of some numbers. The numbers are ordered by
        # certain categories. To use a specific category, return it.
        wimbledon = ["4160", "4241", "4458", "4071", "4422", "4447", "4019", "4042", "4094", "4107"]
        tony_blair = ["3206", "3076", "3331", "3148", "3024", "3358", "3260", "3338", "3169"]
        return tony_blair


