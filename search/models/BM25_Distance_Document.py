from dataclasses import dataclass
from typing import List

from models.Raw_Document import Raw_Document


@dataclass()
class BM25_Distance_Document:
    document: Raw_Document
    BM_25_score: float
    distances_with_user_history: List[float]
