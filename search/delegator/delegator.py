from datetime import datetime
from typing import List

from BM25.BM25Search import BM25Search
from aggregator.aggregator import Aggregator
from database.fetch import fetch_all_documents_from_database, fetch_last_update_time
from models.BM25_Distance_Document import BM25_Distance_Document
from models.BM25_graded_document import BM25_graded_document
from models.Raw_Document import Raw_Document
from user_history.DistanceFetcher import DistanceFetcher

time_of_last_update: datetime = datetime.min


def execute_search(query: str, user_id: str) -> List[Raw_Document]:
    BM25 = BM25Search()
    if (not BM25.is_initialized()) or _should_update():
        all_documents = fetch_all_documents_from_database()
        BM25.build_bm25_model(all_documents)
    search_results: List[BM25_graded_document] = BM25.search_query(query)
    graded_results: List[BM25_Distance_Document] = DistanceFetcher().fetch_document_distance_user_history(
        search_results, user_id)
    final_results: List[Raw_Document] = [result[1] for result in
                                         Aggregator().normalize_and_sort_search_results(graded_results)]
    return final_results


def _should_update() -> bool:
    global time_of_last_update
    last_update_time_database = fetch_last_update_time()
    if last_update_time_database > time_of_last_update:
        time_of_last_update = last_update_time_database
        return True
    else:
        return False
