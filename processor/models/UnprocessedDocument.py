from dataclasses import dataclass

@dataclass()
class UnprocessedDocument:
    document_id: str
    body_raw: str
    title_raw: str
    space: str
