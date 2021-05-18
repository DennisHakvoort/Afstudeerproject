from models.ProcessedDocument import ProcessedDocument
from models.UnprocessedDocument import UnprocessedDocument
from preprocessor.Preprocessor import Preprocessor


class Test_Preprocessor():
    def test_preprocess_documents_success(self, mocker):
        # Setup
        mocker.patch(
            'preprocessor.Preprocessor.get_bool_property',
            return_value=True
        )

        input = UnprocessedDocument(document_id="1",
                                    body_raw="This is a raw body that'll\t have to be cut!!",
                                    title_raw="This is a raw title, please trim me.\n",
                                    space="Moon")
        expected = ProcessedDocument(document_id="1",
                                     body_raw="This is a raw body that'll\t have to be cut!!",
                                     body_preprocessed=" raw body thatll cut",
                                     title_raw="This is a raw title, please trim me.\n",
                                     title_preprocessed=" raw title trim",
                                     space="Moon")
        expected = [expected, expected]
        # run
        actual = Preprocessor().preprocess_documents([input, input])
        # Check
        assert actual == expected
