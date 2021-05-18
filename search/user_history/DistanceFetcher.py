from typing import List

from database.fetch import fetch_document_distances_from_database_from_pairs
from models.BM25_Distance_Document import BM25_Distance_Document
from models.BM25_graded_document import BM25_graded_document
from user_history.HistoryLoader import HistoryLoader


class DistanceFetcher():
    def fetch_document_distance_user_history(self, search_results: List[BM25_graded_document], user_id: str) -> List[
        BM25_Distance_Document]:
        user_history: List[str] = HistoryLoader().retrieve_history(user_id)
        BM25_distances: List[BM25_Distance_Document] = []
        for search_result in search_results:
            document_id_pairs = self._calculate_document_pairs_for_document(search_result, user_history)
            document_distance_for_user_history = self._fetch_distance_for_pairs(document_id_pairs)
            BM25_distances.append(BM25_Distance_Document(
                document=search_result.document,
                BM_25_score=search_result.BM_25_score,
                distances_with_user_history=document_distance_for_user_history
            ))

        return BM25_distances

    def _calculate_document_pairs_for_document(self, search_result: BM25_graded_document, user_history: List[str]) -> \
            List[List[str]]:
        document_id_pairs: List[List[str]] = []
        result_document_id = search_result.document.document_id
        for history_document_id in user_history:
            document_id_pairs.append(sorted([result_document_id, history_document_id]))
        return document_id_pairs

    def _fetch_distance_for_pairs(self, document_id_pairs: List[List[str]]) -> List[float]:
        return fetch_document_distances_from_database_from_pairs(document_id_pairs)
