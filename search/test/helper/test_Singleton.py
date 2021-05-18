import pytest

from helper.Singleton import Singleton


class testClassPleaseIgnore(metaclass=Singleton):
    verifier: int = 0

    def __init__(self, verifier: int):
        self.verifier = verifier


def test_singleton_success():
    # setup
    # Generate a bunch of classes with a different input but verify that the classes are all the same instance.
    instances = []
    expected_verifier = 5
    # run
    for i in range(expected_verifier, expected_verifier+20):
        instances.append(testClassPleaseIgnore(i))
    # check
    for instance in instances:
        assert instance.verifier == expected_verifier
        assert instance == instances[0]
