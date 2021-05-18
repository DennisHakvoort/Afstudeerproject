import logging
from datetime import datetime
from typing import List

from database.connect import connect_to_database
from models.ProcessedDocument import ProcessedDocument

LOG = logging.getLogger(__name__)

FETCH_ALL_DOCUMENTS = "SELECT id, body_raw, body_preprocessed, title_raw, title_preprocessed, space FROM documents"

FETCH_LAST_UPDATE = """
SELECT  last_update FROM last_update
    """


def fetch_all_documents_from_database() -> List[ProcessedDocument]:
    fetched_documents: List[ProcessedDocument] = []
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(FETCH_ALL_DOCUMENTS)
            retrieved_documents = cursor.fetchall()
            for retrieved_document in retrieved_documents:
                fetched_documents.append(ProcessedDocument(
                    document_id=retrieved_document[0],
                    body_raw=retrieved_document[1],
                    body_preprocessed=retrieved_document[2],
                    title_raw=retrieved_document[3],
                    title_preprocessed=retrieved_document[4],
                    space=retrieved_document[5]
                ))

    LOG.info("Retrieved {} documents from the database.".format(len(fetched_documents)))
    return fetched_documents


def fetch_last_update_time() -> datetime:
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(FETCH_LAST_UPDATE)
            last_modification = cursor.fetchone()
            return last_modification[0]
