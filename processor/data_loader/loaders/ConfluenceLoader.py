import logging
from datetime import datetime
from typing import List

import requests

from data_loader.loaders.Loader import Loader
from helper.ConfigReader import get_string_property
from models.UnprocessedDocument import UnprocessedDocument


class ConfluenceLoader(Loader):
    LOG: logging.Logger = None
    _confluence_url = None

    def __init__(self):
        self.LOG = logging.getLogger(__name__)
        self._confluence_url = get_string_property("confluence", "api_base") + \
                               get_string_property("confluence", "api_recent_subpath")

    def retrieve_documents(self, since: datetime) -> List[UnprocessedDocument]:
        fetched_documents: List[UnprocessedDocument] = []
        # By default, python doesn't add the Z to the time, denominating 'zero' or 'zulu', indicating that the time is
        # in the UTC timezone. We add this manually. Without the Z, java doesn't parse the string.
        date_string = since.isoformat() + 'Z'
        params = {"date": date_string}
        request = requests.get(url=self._confluence_url, params=params)

        if request.status_code != 200:
            self.LOG.warning(
                f"Could not fetch pages from the back-end. Request returned with error code {request.status_code}")
            return fetched_documents

        json_data = request.json()
        for page in json_data:
            fetched_documents.append(UnprocessedDocument(
                document_id=page["document_id"],
                body_raw=page["body"],
                title_raw=page["title"],
                space=page["space"]
            ))
        return fetched_documents
