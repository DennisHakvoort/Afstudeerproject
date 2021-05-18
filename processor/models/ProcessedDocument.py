from dataclasses import dataclass


@dataclass()
class ProcessedDocument:
    document_id: str
    body_raw: str
    body_preprocessed: str
    title_raw: str
    title_preprocessed: str
    space: str
