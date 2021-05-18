import logging
from datetime import datetime
from typing import List

from time import time, sleep

from data_loader.DataLoader import DataLoader
from database.fetch import fetch_last_update_time, fetch_all_documents_from_database
from database.store import store_documents_in_database, store_document_distances_in_database, update_last_update_date
from distance.DistanceCalculator import DistanceCalculator
from helper.ConfigReader import get_bool_property, get_int_property
from models.DocumentDistance import DocumentDistance
from models.ProcessedDocument import ProcessedDocument
from models.UnprocessedDocument import UnprocessedDocument
from preprocessor.Preprocessor import Preprocessor

LOG = logging.getLogger(__name__)


def start_data_loading():
    repeat_interval: int = get_int_property("datasource", "automatic_check_interval")

    if get_bool_property("datasource", "automatic_check"):
        start_time = time()
        while True:
            _load_and_process_data()
            time_to_next_iteration = (start_time + repeat_interval) - time()
            if time_to_next_iteration > 0:
                sleep(time_to_next_iteration)
            start_time = time()
    else:
        _load_and_process_data()


def _load_and_process_data():
    '''
    This function loads the data from the datasource and processes it fully. processing includes the following
    steps:
    - Load data from datasource
    - Preprocess data
    - Store preprocessed data in database
    - Calculate distance between preprocessed data
    - Store distance data in database
    :return: Nothing
    '''
    current_update_time = datetime.utcnow()
    last_update_time = fetch_last_update_time()
    new_unprocessed_documents: List[UnprocessedDocument] = DataLoader().retrieve_documents(last_update_time)
    if len(new_unprocessed_documents) > 0:
        new_processed_documents: List[ProcessedDocument] = Preprocessor().preprocess_documents(
            new_unprocessed_documents)
        store_documents_in_database(new_processed_documents)
        all_documents = fetch_all_documents_from_database()
        calculated_distances: List[DocumentDistance] = \
            DistanceCalculator().calculate_distance_documents(all_documents,
                                                              new_processed_documents)
        store_document_distances_in_database(calculated_distances)
        update_last_update_date(current_update_time)
    else:
        LOG.info(f"Checked for new documents, no new documents were found.")
