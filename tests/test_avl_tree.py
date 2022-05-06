from ech_datastructures import AVLTree
import pytest


def test_iter_empty():
    t = AVLTree()
    for _ in t:
        pytest.fail("iterating over an empty tree should not enter the loop")


# TODO: more tests
