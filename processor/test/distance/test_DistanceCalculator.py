from copy import copy

import pytest

from distance.DistanceCalculator import DistanceCalculator
from models.ProcessedDocument import ProcessedDocument


class Test_DistanceCalculator:
    @pytest.fixture(scope="function", autouse=True)
    def _fixture_class(self, mocker):
        mocker.patch(
            'distance.DistanceCalculator.get_bool_property',
            return_value=True
        )
        mocker.patch(
            'distance.DistanceCalculator.spacy.load',
            return_value=None
        )
        # Prevents issues with some 'call once' assertions. Makes behaviour consistent regardless of test
        # execution order. Also pre-loads the dataset.
        DistanceCalculator()
        yield

    def test_calculate_distance_documents_success(self, mocker):
        # Setup
        class fake_nlp_model():
            class fake_text():
                text = "str"
                orth = "ort"

            def __call__(self, *args, **kwargs):
                return [self.fake_text()]

        class fake_calc():
            def nearest_neighbors(self, special, k):
                return [("I am id", 0.334)]

        config_mock_int = mocker.patch(
            'distance.DistanceCalculator.get_int_property',
            side_effect=[10, 50, 500]
        )

        config_mock_bool = mocker.patch(
            'distance.DistanceCalculator.get_bool_property',
            return_value=True
        )

        spacy_mock = mocker.patch(
            'distance.DistanceCalculator.spacy.load',
            return_value=fake_nlp_model()
        )

        wmd_mock = mocker.patch(
            'distance.DistanceCalculator.wmd.WMD',
            return_value=fake_calc()
        )

        input_document_one = ProcessedDocument(
                document_id="one",
                body_raw="unused",
                body_preprocessed="""few word text""",
                title_raw="unused",
                title_preprocessed="title",
                space="big"
            )
        input_document_two = copy(input_document_one)
        input_document_two.document_id = "two"
        input_document_three = copy(input_document_one)
        input_document_three.document_id = "three"
        input_documents = [input_document_one, input_document_two]

        input_documents_all = input_documents + [input_document_three]
        # Run
        DistanceCalculator().__init__()
        distance = DistanceCalculator().calculate_distance_documents(input_documents_all, input_documents)
        # assert
        assert len(distance) == 4
        assert distance[0].distance == 0.334
        assert distance[1].distance == 0
        assert distance[2].distance == 0.334
        assert distance[3].distance == 0
        config_mock_int.assert_has_calls(
            [mocker.call("distance", "amount_of_closest_documents_to_calculate"),
             mocker.call("distance", "vocabulary_min"),
             mocker.call("distance", "vocabulary_max")]
        )
        config_mock_bool.assert_called_once_with("datasource", "is_english")
        spacy_mock.assert_called_once_with("en_core_web_md")
        assert wmd_mock.call_count == 2


    def test_calculate_distance_documents_small_vocab(self, mocker):
        # Setup
        class fake_nlp_model():
            class fake_text():
                text = "str"
                orth = "ort"

            def __call__(self, *args, **kwargs):
                return [self.fake_text()]

        class fake_calc():
            def nearest_neighbors(self, special, k):
                return [("I am id", 0.334)]

        config_mock_int = mocker.patch(
            'distance.DistanceCalculator.get_int_property',
            side_effect=[10, 50, 500]
        )

        config_mock_bool = mocker.patch(
            'distance.DistanceCalculator.get_bool_property',
            return_value=True
        )

        spacy_mock = mocker.patch(
            'distance.DistanceCalculator.spacy.load',
            return_value=fake_nlp_model()
        )

        wmd_mock = mocker.patch(
            'distance.DistanceCalculator.wmd.WMD',
            side_effect=ValueError
        )
        input_document_one = ProcessedDocument(
                document_id="one",
                body_raw="unused",
                body_preprocessed="""few word text""",
                title_raw="unused",
                title_preprocessed="title",
                space="big"
            )
        input_document_two = copy(input_document_one)
        input_document_two.document_id = "two"

        input_documents = [input_document_one, input_document_two]
        # Run
        DistanceCalculator().__init__()
        distance = DistanceCalculator().calculate_distance_documents(input_documents, input_documents)
        # assert
        assert len(distance) == 0
        config_mock_int.assert_has_calls(
            [mocker.call("distance", "amount_of_closest_documents_to_calculate"),
             mocker.call("distance", "vocabulary_min"),
             mocker.call("distance", "vocabulary_max")]
        )
        config_mock_bool.assert_called_once_with("datasource", "is_english")
        spacy_mock.assert_called_once_with("en_core_web_md")
        assert wmd_mock.call_count == 2
