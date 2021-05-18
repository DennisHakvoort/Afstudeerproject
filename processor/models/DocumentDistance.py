from dataclasses import dataclass


@dataclass()
class DocumentDistance:
    document_id_1: str
    document_id_2: str
    distance: float
