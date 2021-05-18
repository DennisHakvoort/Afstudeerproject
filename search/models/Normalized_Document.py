from dataclasses import dataclass
from typing import List

from models.Raw_Document import Raw_Document


@dataclass()
class Normalized_Document:
    document: Raw_Document
    normalized_BM_25_score: float
    normalized_distances_with_user_history: float
