import logging
import string
from typing import List

import spacy
from spacy.tokens.doc import Doc

from helper.ConfigReader import get_bool_property



stopwords: List[str] = []
nlp_model = None
LOG = logging.getLogger(__name__)


def _initiate_language_data():
    global nlp_model
    global stopwords
    is_english = get_bool_property('datasource', 'is_english')
    if (is_english):
        nlp_model = spacy.load("en_core_web_sm")
        #  An English dataset is unlikely to contain many Dutch text, Dutch stopwords are not merged with the English ones.
        stopwords = nlp_model.Defaults.stop_words
    else:
        nlp_model = spacy.load("nl_core_news_sm")
        #  Dutch people love the English language, a lot of of our people write in English, so if we're processing
        #  Dutch text, we also filter out the English stopwords.
        stopwords = nlp_model.Defaults.stop_words | spacy.load("en_core_web_sm").Defaults.stop_words

def preprocess_string(text: str):
    if nlp_model is None:
        _initiate_language_data()
    text = _remove_punctuation_from_string(text)
    text = _reduce_excessive_whitespace_from_string(text)
    doc: Doc = nlp_model(text)
    preprocessed_text: str = ""
    for word in doc:
        # remove the word if it's a stop word
        if word.lower_ in stopwords:
            continue
        else:
            # Adding the word lemmas back into a string, with a space between the previous word
            preprocessed_text += (" " + word.lemma_)
    return preprocessed_text

def _remove_punctuation_from_string(input_string: str) -> str:
    return input_string.translate(str.maketrans('', '', string.punctuation))

def _reduce_excessive_whitespace_from_string(input_string: str) -> str:
    return " ".join(input_string.split())
