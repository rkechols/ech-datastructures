from ech_datastructures import AVLTree
import pytest


def assert_empty(avl: AVLTree):
    assert len(avl) == 0, "empty tree should have length 0"
    assert avl.is_empty(), "empty tree should be marked as empty"
    assert not avl.remove(5), "removing from an empty tree should return False"
    for _ in avl:
        pytest.fail("iterating over an empty tree should not enter the loop")


def test_empty_tree():
    avl = AVLTree()
    assert_empty(avl)


def test_add_many_nums():
    nums = [5, 4, 7, 8, 4, 6, 2, 7, 1]
    avl = AVLTree()
    added = set()
    for num in nums:
        if num in added:
            assert not avl.add(num), "should return False to mark failed addition (duplicate)"
        else:
            assert avl.add(num), "should return True to mark a successful addition"
            added.add(num)
        assert len(avl) == len(added)
        assert list(avl) == sorted(added), \
            "iterating over tree should return numbers in order, and with no duplicates"


# TODO: tests about balance?
