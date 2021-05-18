import pytest

from BM25.preprocess_query import preprocess_string


class Test_preprocess_query():
    def test_preprocess_string(self, mocker):
        # Setup
        mocker.patch(
            'BM25.preprocess_query.get_bool_property',
            return_value=True
        )
        input = "This is a long and fuzzy string, we need to remove the fluff"
        expected = " long fuzzy string need remove fluff"
        # Run
        actual = preprocess_string(input)
        # Check
        assert actual == expected