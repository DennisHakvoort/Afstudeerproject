from dataclasses import dataclass

from models.Raw_Document import Raw_Document


@dataclass()
class BM25_graded_document:
    document: Raw_Document
    BM_25_score: float
