from dataclasses import dataclass


@dataclass()
class Raw_Document:
    document_id: str
    body_raw: str
    title_raw: str
    space: str
