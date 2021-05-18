import datetime
import logging
from collections import Counter
from typing import List

import numpy
import spacy
import wmd
from time import time

from helper.ConfigReader import get_bool_property, get_int_property
from helper.Singleton import Singleton
from models.DocumentDistance import DocumentDistance
from models.ProcessedDocument import ProcessedDocument


class DistanceCalculator(metaclass=Singleton):
    nlp_model = None
    LOG = logging.getLogger()

    def __init__(self):
        self._load_data_set()

    def calculate_distance_documents(self, all_documents: List[ProcessedDocument],
                                     new_documents: List[ProcessedDocument]) -> List[DocumentDistance]:
        nbow = self._convert_documents_to_nbow(all_documents)
        amount_of_closest_documents = get_int_property("distance", "amount_of_closest_documents_to_calculate")
        vocabulary_min = get_int_property("distance", "vocabulary_min")
        vocabulary_max = get_int_property("distance", "vocabulary_max")

        calculated_distances: List[DocumentDistance] = []
        documents_length = len(new_documents)
        finished_operations = 0

        start_time = time()
        for document in new_documents:
            # add newly calculated distances to 'document' to the end of 'calculated_distances'
            calculated_distances.extend(self._calculate_nearest_documents_to(nbow,
                                                                             document.document_id,
                                                                             amount_of_closest_documents,
                                                                             vocabulary_min,
                                                                             vocabulary_max))
            finished_operations += 1
            avg_calculation_time = (time() - start_time) / finished_operations
            time_left = (documents_length - finished_operations) * avg_calculation_time
            self.LOG.debug(
                "calculated distance of {} out of {}, {}%. Average time per calculation: {}s, time left: {}".format(
                    finished_operations,
                    documents_length,
                    format(finished_operations / documents_length * 100, ".2f"),
                    avg_calculation_time,
                    str(datetime.timedelta(seconds=time_left))))
        print(calculated_distances)
        return calculated_distances

    def _load_data_set(self):
        # TODO: STAGE-1676 Right now, we load external data sets from spacy. In the future research should be done to
        # check if it's possible to use more advanced, word2vec specific datasets.
        if get_bool_property("datasource", "is_english"):
            self.nlp_model = spacy.load('en_core_web_md')
        else:
            self.nlp_model = spacy.load('nl_core_news_md')

    def _convert_documents_to_nbow(self, documents):
        '''
        Converts the documents to a neutral bag of words (nbow) model. The specific format of this model is dictated by
        the relaxed wmd package that's used to calculate the distances.
        https://github.com/src-d/wmd-relax#usage

        it follows the following format:
        nbow[document_id] = (document_id, <list of hash id's referencing to positions in the dict of the NLP model used>
            , <amount of times the word at position x in the list of id's appeared in the text, this array is in a float32 format>)
        '''
        nbow = {}
        for document in documents:
            text = document.body_preprocessed + document.title_preprocessed
            tokens_in_nlp_format = [token for token in self.nlp_model(text)]
            words_and_their_occurences_in_text = Counter(token.text for token in tokens_in_nlp_format)
            words_and_dict_id = {token.text: token.orth for token in tokens_in_nlp_format}
            unique_words_in_text = numpy.unique([token.text for token in tokens_in_nlp_format])
            nbow[document.document_id] = (
                document.document_id, [words_and_dict_id[word] for word in unique_words_in_text],
                numpy.array([words_and_their_occurences_in_text[word] for word in unique_words_in_text],
                            dtype=numpy.float32))
        return nbow

    def _calculate_nearest_documents_to(self, nbow, comparison_document_id, amount_of_closest_neighbours,
                                        vocabulary_min, vocabulary_max) \
            -> List[DocumentDistance]:
        nlp_model = self.nlp_model

        # A hook necessary for WMD to get the vectors of the words from the spacy model.
        class SpacyEmbeddings(object):
            def __getitem__(self, item):
                return nlp_model.vocab[item].vector

        distances: List[DocumentDistance] = []

        try:
            calc = wmd.WMD(SpacyEmbeddings(), nbow, vocabulary_min=vocabulary_min, vocabulary_max=vocabulary_max)
            for title, relevance in calc.nearest_neighbors(comparison_document_id, k=amount_of_closest_neighbours):
                sorted_document_ids = sorted([title, comparison_document_id])
                distances.append(DocumentDistance(
                    document_id_1=sorted_document_ids[0],
                    document_id_2=sorted_document_ids[1],
                    distance=relevance
                ))

            # A document will have a distance of 0 with itself, we include this in the results.
            distances.append(DocumentDistance(
                document_id_1=comparison_document_id,
                document_id_2=comparison_document_id,
                distance=0
            ))
        # In the event that a document's vocabulary is too large or to small, a ValueError is thrown.
        except ValueError as e:
            self.LOG.info(
                "Skipped distance calculation of document #{}, exception: {}".format(comparison_document_id, e))

        return distances
