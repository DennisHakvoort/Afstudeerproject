from configparser import NoSectionError

import pytest

from helper import ConfigReader
from helper.ConfigReader import get_string_property, get_bool_property, get_int_property, get_float_property
from helper.paths import get_root_dir


class Test_ConfigReader:
    ini_location = get_root_dir().joinpath("config", "config.ini")

    @pytest.fixture(autouse=True)
    def _clean_config_cache(self):
        ConfigReader.config_file = None
        yield

    # Since we're never quite certain what config.ini contains, we have to add our own value and delete it afterwards.
    # This tests adds two lines and deletes them afterwards. The only problem it leaves behind a new whiteline after
    # each run. I can't seem to get rid of that yet.
    def test_get_property_success(self):
        # setup
        expected = "completedness"

        with open(self.ini_location, "a") as config:
            config.write("\n[test]\nvalue={}".format(expected))
        # run
        actual = get_string_property("test", "value")
        # breakdown
        file = None
        with open(self.ini_location, "r") as config:
            file = config.readlines()
        with open(self.ini_location, "w") as config:
            [config.write(line) for line in file[:-2]]
        # check
        assert actual == expected

    def test_get_property_nonexistent_property(self):
        # run
        with pytest.raises(NoSectionError):
            get_string_property("test", "value")

    def test_get_property_nonexistent_file(self, _fixture_test_get_property_nonexistent_file):
        # run
        # While this section/option combination doesn't exist, it won't matter for this specific test.
        # The rather interesting syntax is thanks to pytest:
        # https://docs.pytest.org/en/stable/assert.html#assertions-about-expected-exceptions
        with pytest.raises(SystemExit):
            def test():
                get_string_property("test", "value")

            test()

    @pytest.fixture(scope="function")
    def _fixture_test_get_property_nonexistent_file(self):
        new_ini_location = self.ini_location.rename(self.ini_location.with_suffix(".backup"))
        yield
        new_ini_location.rename(self.ini_location.with_suffix(".ini"))

    def test_get_string_property_success(self, mocker):
        # Setup
        input = "string"
        expected = input
        read_property_mock = mocker.patch(
            "helper.ConfigReader._read_property",
            return_value = input
        )
        # Run
        actual = get_string_property("test", "parameters")
        # Check
        assert actual == expected
        read_property_mock.assert_called_once_with("test", "parameters")

    def test_get_bool_property_success(self, mocker):
        # Setup
        input = "TrUe"
        expected = True
        read_property_mock = mocker.patch(
            "helper.ConfigReader._read_property",
            return_value = input
        )
        # Run
        actual = get_bool_property("test", "parameters")
        # Check
        assert actual == expected
        read_property_mock.assert_called_once_with("test", "parameters")

    def test_get_int_property_success(self, mocker):
        # Setup
        input = "3"
        expected = 3
        read_property_mock = mocker.patch(
            "helper.ConfigReader._read_property",
            return_value = input
        )
        # Run
        actual = get_int_property("test", "parameters")
        # Check
        assert actual == expected
        read_property_mock.assert_called_once_with("test", "parameters")

    def test_get_float_property_success(self, mocker):
        # Setup
        input = "2.98"
        expected = 2.98
        read_property_mock = mocker.patch(
            "helper.ConfigReader._read_property",
            return_value = input
        )
        # Run
        actual = get_float_property("test", "parameters")
        # Check
        assert actual == expected
        read_property_mock.assert_called_once_with("test", "parameters")