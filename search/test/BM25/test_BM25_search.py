from copy import copy

from BM25.BM25Search import BM25Search
from models.BM25_graded_document import BM25_graded_document
from models.Preprocessed_Document import Preprocessed_Document
from models.Raw_Document import Raw_Document


class Test_BM25_search():
    def test_build_bm25_model_success(self, mocker):
        # setup
        okapi_mock = mocker.patch(
            'BM25.BM25Search.BM25Okapi'
        )

        expected_document_one = Preprocessed_Document(
            document_id="one",
            body_raw="a raw body",
            body_preprocessed="a preprocessed body",
            title_raw="a raw title",
            title_preprocessed="a preprocessed title",
            space="space"
        )

        expected_document_two = copy(expected_document_one)
        expected_document_two.document_id = "two"

        expected_documents = [
            expected_document_one,
            expected_document_two
        ]

        expected_strings = [['a', 'preprocessed', 'title', 'a', 'preprocessed', 'body'],
                            ['a', 'preprocessed', 'title', 'a', 'preprocessed', 'body']]
        # run
        BM25_instance = BM25Search()
        BM25_instance.build_bm25_model(expected_documents)
        # check
        assert BM25_instance._indexed_documents == expected_documents
        okapi_mock.assert_called_once_with(expected_strings)

    def test_search_query_success(self, mocker):
        # Setup
        def fake_preprocessor(string):
            return string

        preprocessor_mock = mocker.patch(
            'BM25.BM25Search.preprocess_string',
            side_effect=fake_preprocessor
        )

        expected_document_one = Preprocessed_Document(
            document_id="one",
            body_raw="a raw body",
            body_preprocessed="a preprocessed body",
            title_raw="a raw title",
            title_preprocessed="a preprocessed title",
            space="space"
        )

        expected_document_two = copy(expected_document_one)
        expected_document_two.document_id = "two"

        expected_document_three = copy(expected_document_one)
        expected_document_three.document_id = "three"

        input_documents = [
            expected_document_one,
            expected_document_two,
            expected_document_three
        ]

        config_mock = mocker.patch(
            'BM25.BM25Search.get_float_property',
            return_value=1.0
        )

        expected_result_one = Raw_Document(document_id='three',
                                           body_raw='a raw body',
                                           title_raw='a raw title',
                                           space='space')

        expected_result_two = copy(expected_result_one)
        expected_result_two.document_id = "one"

        expected_results = [
            BM25_graded_document(
                document=expected_result_one,
                BM_25_score=1.22),
            BM25_graded_document(
                document=expected_result_two,
                BM_25_score=1.12)
        ]

        class fake_BM25():
            received_strings = None

            def get_scores(self, strings):
                self.received_strings = strings
                return [1.12, 0.23, 1.22]

        BM25_instance = BM25Search()
        BM25_instance._BM25_model = fake_BM25()
        BM25_instance._indexed_documents = input_documents

        input_query = "test query"

        # Run
        received_results = BM25_instance.search_query(input_query)

        # Check
        config_mock.assert_called_once_with("search", "threshold")
        preprocessor_mock.assert_called_once_with(input_query)
        assert BM25_instance._BM25_model.received_strings == ["test", "query"]
        assert received_results == expected_results

    def test_is_initialized_success(self):
        # Setup
        BM25_instance = BM25Search()
        BM25_instance._BM25_model = "not none"
        expected = True
        # Run
        actual = BM25_instance.is_initialized()
        # Check
        assert actual == expected

    def test_is_initialized_not_initialized(self):
        # Setup
        BM25_instance = BM25Search()
        BM25_instance._BM25_model = None
        expected = False
        # Run
        actual = BM25_instance.is_initialized()
        # Check
        assert actual == expected
