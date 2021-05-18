from datetime import datetime

import pytest

from data_loader.loaders.BBCLoader import BBCLoader
from models.UnprocessedDocument import UnprocessedDocument


class Test_BBCLoader:
    def test_get_data_success(self, mocker):
        # Setup
        mocker.patch(
            'data_loader.loaders.BBCLoader.get_string_property',
            return_value="test/data/BBC"
        )

        loader = BBCLoader()
        expected = [UnprocessedDocument(document_id="1000",
                                        body_raw=" It doesn't contain much interesting.  Thank you for listening to my presentation.",
                                        title_raw='This is a test file',
                                        space='BBC')]
        last_update = datetime.now()
        # Run
        actual = loader.retrieve_documents(last_update)
        # Check
        assert actual == expected

    def test_get_data_nonexistent_directory(self, mocker):
        # Setup
        mocker.patch(
            'data_loader.loaders.BBCLoader.get_string_property',
            return_value="test/data/this/path/does/not/exist"
        )

        loader = BBCLoader()
        # Run
        with pytest.raises(Exception):
            def test():
                loader.retrieve_documents()

            test()
