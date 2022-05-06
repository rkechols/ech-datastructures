from typing import List, Set, Tuple
import copy

import pytest

from ech_datastructures import AVLTree


@pytest.fixture(scope="function")
def nums() -> List[int]:
    return [5, 4, 7, 8, 4, 6, 2, 7, 1]


@pytest.fixture(scope="function")
def avl_filled(nums: List[int]) -> Tuple[AVLTree, Set[int]]:
    avl = AVLTree()
    for num in nums:
        avl.add(num)
    return avl, set(nums)


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


def test_remove_many_nums(avl_filled: Tuple[AVLTree, Set[int]]):
    avl, nums_original = avl_filled
    nums_remaining = copy.copy(nums_original)
    bogus = max(nums_remaining) + 2
    while len(nums_remaining) > 0:
        num = nums_remaining.pop()
        assert avl.remove(num), "should return True to mark successful removal"
        assert len(avl) == len(nums_remaining)
        assert list(avl) == sorted(nums_remaining), \
            "iterating over tree should return numbers in order, and with no duplicates"
        assert not avl.remove(bogus), "should return False to mark failed removal"
    assert_empty(avl)
    for num in nums_original:
        assert not avl.remove(num), "should return False to mark failed removal"

# TODO: tests about balance?
