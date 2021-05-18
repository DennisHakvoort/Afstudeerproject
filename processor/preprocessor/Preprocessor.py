import logging
import string
from time import time
from typing import List

import spacy
from spacy.tokens.doc import Doc

from helper.ConfigReader import get_bool_property
from helper.Singleton import Singleton
from models.ProcessedDocument import ProcessedDocument
from models.UnprocessedDocument import UnprocessedDocument


class Preprocessor(metaclass=Singleton):
    _stopwords: List[str] = []
    _nlp_model = None
    LOG = logging.getLogger(__name__)

    def __init__(self):
        self._initiate_language_data()

    def _initiate_language_data(self):
        is_english = get_bool_property('datasource', 'is_english')
        if (is_english):
            self._nlp_model = spacy.load("en_core_web_md")
            #  An English dataset is unlikely to contain many Dutch text, Dutch stopwords are not merged with the English ones.
            self._stopwords = self._nlp_model.Defaults.stop_words
        else:
            self._nlp_model = spacy.load("nl_core_news_md")
            #  Dutch people love the English language, a lot of of our people write in English, so if we're processing
            #  Dutch text, we also filter out the English stopwords.
            self._stopwords = self._nlp_model.Defaults.stop_words | spacy.load("en_core_web_md").Defaults.stop_words

    def preprocess_documents(self, documents: List[UnprocessedDocument]) -> List[ProcessedDocument]:
        finished_documents: List[ProcessedDocument] = []
        document_length = len(documents)
        self.LOG.debug("Beginning document preprocessing...")
        start_time = time()
        for index, document in enumerate(documents):
            processed_document = ProcessedDocument(
                document_id=document.document_id,
                body_raw=document.body_raw,
                body_preprocessed=self._preprocess_string(document.body_raw),
                title_raw=document.title_raw,
                title_preprocessed=self._preprocess_string(document.title_raw),
                space=document.space
            )
            finished_documents.append(processed_document)
            self.LOG.debug("Finished preprocessing of document {} out of {}. ({}%)".format(
                index, document_length, format(index / document_length * 100, ".2f")))
        self.LOG.info("Finished document preprocessing in %0.3fs" % (time() - start_time))
        return finished_documents

    def _preprocess_string(self, text: str):
        text = self._remove_punctuation_from_string(text)
        text = self._reduce_excessive_whitespace_from_string(text)
        doc: Doc = self._nlp_model(text)
        preprocessed_text: str = ""
        for word in doc:
            # remove the word if it's a stop word
            if word.lower_ in self._stopwords:
                continue
            else:
                # Adding the word lemmas back into a string, with a space between the previous word
                preprocessed_text += (" " + word.lemma_)
        return preprocessed_text

    def _remove_punctuation_from_string(self, input_string: str) -> str:
        return input_string.translate(str.maketrans('', '', string.punctuation))

    def _reduce_excessive_whitespace_from_string(self, input_string: str) -> str:
        return " ".join(input_string.split())
