from typing import List

from rank_bm25 import BM25Okapi

from BM25.preprocess_query import preprocess_string
from helper.ConfigReader import get_float_property, get_int_property
from helper.Singleton import Singleton
from models.BM25_graded_document import BM25_graded_document
from models.Preprocessed_Document import Preprocessed_Document
from models.Raw_Document import Raw_Document


class BM25Search(metaclass=Singleton):
    _BM25_model = None
    _indexed_documents: List[Preprocessed_Document] = []

    def build_bm25_model(self, documents: List[Preprocessed_Document]):
        tokenized_document_strings: List[List[str]] = []
        for document in documents:
            search_string = document.title_preprocessed + " " + document.body_preprocessed
            tokenized_document_strings.append(search_string.lower().split())
        self._BM25_model = BM25Okapi(tokenized_document_strings)
        self._indexed_documents = documents

    def search_query(self, query: str) -> List[BM25_graded_document]:
        amount_to_return = get_int_property("search", "number_of_results")
        inclusion_threshold: float = get_float_property("search", "threshold")

        preprocessed_query = preprocess_string(query)
        documents_above_threshold: List[BM25_graded_document] = []
        print(preprocessed_query)
        scores = self._BM25_model.get_scores(preprocessed_query.lower().split())
        for i, score in enumerate(scores):
            if score >= inclusion_threshold:
                corresponding_document = self._indexed_documents[i]
                corresponding_document_raw = Raw_Document(
                    document_id=corresponding_document.document_id,
                    body_raw=corresponding_document.body_raw,
                    title_raw=corresponding_document.title_raw,
                    space=corresponding_document.space,
                )
                documents_above_threshold.append(BM25_graded_document(
                    document=corresponding_document_raw,
                    BM_25_score=score
                ))
        return sorted(documents_above_threshold, key=lambda doc: doc.BM_25_score, reverse=True)[:amount_to_return]

    def is_initialized(self) -> bool:
        return self._BM25_model is not None
