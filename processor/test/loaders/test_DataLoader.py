from datetime import datetime

import pytest

from data_loader import DataLoader


class Test_DataLoader:
    @pytest.fixture(scope="class")
    def _fixture_class(self):
        # Prevents issues with some 'call once' assertions. Makes behaviour consistent regardless of test
        # execution order, because the dataloader will always have an instance in it's singleton already.
        DataLoader.DataLoader()
        yield
        pass

    def test_get_data_success(self, mocker, _fixture_class):
        # Setup
        expected = "Rare occurrence of succeeded test found."

        config_mock = mocker.patch(
            'data_loader.DataLoader.get_string_property',
            return_value="BBC"
        )

        bbc_mock = mocker.patch(
            'data_loader.DataLoader.BBCLoader.retrieve_documents',
            return_value=expected
        )

        last_update_time = datetime.now()

        # Run
        # This is rather unorthodox, but if we call the retrieve_documents method directly, the singleton
        # would take over and give us an object from a previous test, thus resulting in a possibly
        # different datasource and ruining the test.
        DataLoader.DataLoader().__init__()
        actual = DataLoader.DataLoader().retrieve_documents(last_update_time)
        # Check
        config_mock.assert_called_once_with("datasource", "data_source")
        bbc_mock.assert_called_once()
        assert expected == actual

    def test_get_data_nonexistent_dataloader(self, mocker, _fixture_class):
        # Setup
        # DataLoader.DataLoader()._instances = {}
        config_mock = mocker.patch(
            'data_loader.DataLoader.get_string_property',
            return_value="IDONTEXIST"
        )

        # Run
        with pytest.raises(ValueError):
            def test():
                DataLoader.DataLoader().__init__()

            test()

        # Check
        config_mock.assert_called_with("datasource", "data_source")
        assert config_mock.call_count == 2
