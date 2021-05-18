import math
from typing import List, Tuple

from helper.ConfigReader import get_float_property, get_int_property
from models.BM25_Distance_Document import BM25_Distance_Document
from models.Normalized_Document import Normalized_Document
from models.Raw_Document import Raw_Document


class Aggregator():
    _bm25_weight = get_int_property("weight", "bm25_weight")
    _distance_weight = get_int_property("weight", "distance_weight")

    def normalize_and_sort_search_results(self, search_results: List[Raw_Document]):
        normalized_search_results: List[Normalized_Document] = self._normalize_search_results(search_results)
        weighted_results: List[Tuple[float, Raw_Document]] = self._apply_weights_on_results(normalized_search_results)
        sorted_results = [result for result in sorted(weighted_results, key=lambda item: item[0], reverse=True)]
        return sorted_results

    def _sigmoid(self, value: float, midpoint: float, stretch: float) -> float:
        return math.atan(((value - midpoint) * stretch)) * (math.pi * 0.1) + 0.5

    def _normalize_search_results(self, search_results: List[BM25_Distance_Document]) -> List[Normalized_Document]:
        normalized_search_results: List[Normalized_Document] = []
        for result in search_results:
            normalized_BM25_score = self._normalize_BM25_result(result.BM_25_score)
            normalized_distance: float = self._normalize_distance_results(result.distances_with_user_history)
            normalized_search_results.append(Normalized_Document(
                document=result.document,
                normalized_BM_25_score=normalized_BM25_score,
                normalized_distances_with_user_history=normalized_distance
            ))
        return normalized_search_results

    def _normalize_BM25_result(self, BM25_score: float) -> float:
        midpoint = get_float_property("normalization", "bm25_midpoint")
        stretch = get_float_property("normalization", "bm25_stretch")
        return self._sigmoid(BM25_score, midpoint, stretch)

    def _normalize_distance_results(self, distances: List[float]) -> float:
        if len(distances) == 0:
            return 0.0
        midpoint = get_float_property("normalization", "distance_midpoint")
        stretch = get_float_property("normalization", "distance_stretch")
        total_distance = 0.0
        for distance in distances:
            total_distance += self._sigmoid(distance, midpoint, stretch)
        return total_distance / len(distances)

    def _apply_weights_on_results(self, normalized_search_results: List[Normalized_Document]) -> List[
            Tuple[float, Raw_Document]]:
        weighted_results: List[Tuple[float, Raw_Document]] = []
        for search_result in normalized_search_results:
            total = 0.0
            total += search_result.normalized_BM_25_score * self._bm25_weight
            total += search_result.normalized_distances_with_user_history * self._distance_weight
            weighted_results.append((total, search_result.document))
        return weighted_results
