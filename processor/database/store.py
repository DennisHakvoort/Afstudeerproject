import logging
from datetime import datetime
from time import time
from typing import List

import psycopg2

from database.connect import connect_to_database
from models.DocumentDistance import DocumentDistance
from models.ProcessedDocument import ProcessedDocument

# This file is not tested. If this file ever gets to contain some complicated insert statements I'll have a look at
# including it in the unit tests. I don't think this file is complicated enough to warrant the time it takes to
# setup the tests for a database.

UPSERT_DOCUMENT = """
INSERT INTO documents ( id, 
                        body_raw, 
                        body_preprocessed,
                        title_raw, 
                        title_preprocessed, 
                        space) 
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE 
SET body_raw = excluded.body_raw, 
    body_preprocessed= excluded.body_preprocessed,
    title_raw = excluded.title_raw,
    title_preprocessed = excluded.title_preprocessed,
    space = excluded.space;
                """

UPSERT_DOCUMENT_DISTANCE = """
                INSERT INTO document_distance ( document_id_1, 
                                                document_id_2, 
                                                distance)
                VALUES (%s, %s, %s)
                ON CONFLICT (document_id_1, document_id_2) DO UPDATE 
                SET distance = excluded.distance;
                """

UPDATE_LAST_UPDATE = """
UPDATE last_update
SET    last_update = %s
"""


LOG = logging.getLogger(__name__)


def store_documents_in_database(documents: List[ProcessedDocument]):
    document_count = len(documents)
    LOG.debug("Beginning database insertion of {} documents...".format(document_count))
    start_time = time()
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                for index, doc in enumerate(documents):
                    upsert_document_query = UPSERT_DOCUMENT
                    upsert_document_data = (doc.document_id,
                                            doc.body_raw,
                                            doc.body_preprocessed,
                                            doc.title_raw,
                                            doc.title_preprocessed,
                                            doc.space)
                    cursor.execute(upsert_document_query, upsert_document_data)
            connection.commit()
    except psycopg2.Error as error:
        LOG.warning("Insertion of documents failed. Error: {}".format(str(error)))

    LOG.info(
        "Finished database insertion of {} documents in {}s"
            .format(document_count, "%0.3f" % (time() - start_time)))


def store_document_distances_in_database(distances: List[DocumentDistance]):
    document_count = len(distances)
    LOG.debug("Beginning database insertion of {} document distances...".format(document_count))
    start_time = time()
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                for distance in distances:
                    upsert_document_query = UPSERT_DOCUMENT_DISTANCE
                    upsert_document_data = (distance.document_id_1,
                                            distance.document_id_2,
                                            distance.distance)
                    cursor.execute(upsert_document_query, upsert_document_data)
            connection.commit()
    except psycopg2.Error as error:
        LOG.warning("Insertion of document distances failed. Error: {}".format(str(error)))

    LOG.info(
        "Finished database insertion of {} document distances in {}s".format(document_count,
                                                                             "%0.3f" % (time() - start_time)))

def update_last_update_date(date: datetime):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                upsert_document_query = UPDATE_LAST_UPDATE
                upsert_document_data = (date,)
                cursor.execute(upsert_document_query, upsert_document_data)
            connection.commit()
    except psycopg2.Error as error:
        LOG.warning("Insertion of last update failed. Error: {}".format(str(error)))

