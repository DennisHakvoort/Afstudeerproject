from delegator.delegator import start_data_loading
from models.DocumentDistance import DocumentDistance
from models.ProcessedDocument import ProcessedDocument
from models.UnprocessedDocument import UnprocessedDocument


class Test_delegator:

    def test_start_data_loading_success(self, mocker):
        # Setup
        config_int_mock = mocker.patch(
            "delegator.delegator.get_int_property",
            return_value=1
        )
        config_bool_mock = mocker.patch(
            "delegator.delegator.get_bool_property",
            return_value=False
        )

        expected_document = UnprocessedDocument(
            document_id="14",
            body_raw="A raw body",
            title_raw="A raw title",
            space="Milky way"
        )
        expected_documents = [expected_document, expected_document]

        loader_mock = mocker.patch(
            'delegator.delegator.DataLoader.retrieve_documents',
            return_value=expected_documents
        )

        expected_processed_document = ProcessedDocument(
            document_id=14,
            body_raw="A raw body",
            body_preprocessed="A not so raw body",
            title_raw="A raw title",
            title_preprocessed="A not so raw title",
            space="Milky way"
        )
        expected_processed_documents = [expected_processed_document, expected_processed_document]

        preprocessor_mock = mocker.patch(
            "delegator.delegator.Preprocessor.preprocess_documents",
            return_value=expected_processed_documents
        )

        store_documents_mock = mocker.patch(
            "delegator.delegator.store_documents_in_database"
        )

        expected_stored_document = UnprocessedDocument(
            document_id="154",
            body_raw="A raw body 2",
            title_raw="A raw title 2",
            space="Milky ways"
        )
        expected_all_documents = expected_documents + [expected_stored_document]

        fetch_documents_mock = mocker.patch(
            "delegator.delegator.fetch_all_documents_from_database",
            return_value=expected_all_documents
        )

        expected_distance = DocumentDistance(
            document_id_1="one",
            document_id_2="two",
            distance=3.4234553
        )

        expected_distances = [expected_distance, expected_distance]

        distance_mock = mocker.patch(
            "delegator.delegator.DistanceCalculator.calculate_distance_documents",
            return_value=expected_distances
        )

        store_distance_mock = mocker.patch(
            "delegator.delegator.store_document_distances_in_database"
        )

        update_mock = mocker.patch(
            "delegator.delegator.update_last_update_date",
        )

        # Run
        start_data_loading()
        # Check
        config_int_mock.assert_called_once_with("datasource", "automatic_check_interval")
        config_bool_mock.assert_called_once_with("datasource", "automatic_check")
        loader_mock.assert_called_once()
        preprocessor_mock.assert_called_once_with(expected_documents)
        store_documents_mock.assert_called_once_with(expected_processed_documents)
        fetch_documents_mock.assert_called_once()
        distance_mock.assert_called_once_with(expected_all_documents, expected_processed_documents)
        store_distance_mock.assert_called_once_with(expected_distances)
        update_mock.assert_called_once()

    def test_start_data_loading_no_documents_found(self, mocker):
        # Setup
        config_int_mock = mocker.patch(
            "delegator.delegator.get_int_property",
            return_value=1
        )
        config_bool_mock = mocker.patch(
            "delegator.delegator.get_bool_property",
            return_value=False
        )

        expected_documents = []

        loader_mock = mocker.patch(
            'delegator.delegator.DataLoader.retrieve_documents',
            return_value=expected_documents
        )

        update_mock = mocker.patch(
            "delegator.delegator.update_last_update_date",
        )
        # Run
        start_data_loading()
        # Check
        config_int_mock.assert_called_once_with("datasource", "automatic_check_interval")
        config_bool_mock.assert_called_once_with("datasource", "automatic_check")
        loader_mock.assert_called_once()
        update_mock.assert_not_called()
