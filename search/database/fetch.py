import logging
from datetime import datetime
from typing import List

from database.connect import connect_to_database
from models.Preprocessed_Document import Preprocessed_Document

LOG = logging.getLogger(__name__)

FETCH_ALL_DOCUMENTS = "SELECT id, body_raw, body_preprocessed, title_raw, title_preprocessed, space FROM documents"

FETCH_DISTANCE_FOR_PAIR = """
SELECT  distance FROM document_distance
WHERE   document_id_1 = %s
    AND document_id_2 = %s;
    """

FETCH_LAST_UPDATE = """
SELECT  last_update FROM last_update
    """


def fetch_all_documents_from_database() -> List[Preprocessed_Document]:
    fetched_documents: List[Preprocessed_Document] = []
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(FETCH_ALL_DOCUMENTS)
            retrieved_documents = cursor.fetchall()
            for retrieved_document in retrieved_documents:
                fetched_documents.append(Preprocessed_Document(
                    document_id=retrieved_document[0],
                    body_raw=retrieved_document[1],
                    body_preprocessed=retrieved_document[2],
                    title_raw=retrieved_document[3],
                    title_preprocessed=retrieved_document[4],
                    space=retrieved_document[5]
                ))

    LOG.info("Retrieved {} documents from the database.".format(len(fetched_documents)))

    return fetched_documents


def fetch_document_distances_from_database_from_pairs(document_id_pairs: List[List[str]]) -> List[float]:
    fetched_distances: List[float] = []
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            for document_id_pair in document_id_pairs:
                cursor.execute(FETCH_DISTANCE_FOR_PAIR, document_id_pair)
                if cursor.rowcount > 0:
                    distance = cursor.fetchone()
                    fetched_distances.append(distance[0])
    return fetched_distances


def fetch_last_update_time() -> datetime:
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(FETCH_LAST_UPDATE)
            last_modification = cursor.fetchone()
            return last_modification[0]
