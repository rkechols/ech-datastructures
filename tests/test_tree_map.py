import copy
import random
from typing import List, Set, Tuple

import pytest

from ech_datastructures import TreeMap


@pytest.fixture(scope="function")
def nums() -> List[int]:
    return [5, 4, 7, 8, 4, 6, 2, 7, 1]


@pytest.fixture(scope="function")
def tree_filled(nums: List[int]) -> Tuple[TreeMap, Set[int]]:
    tree = TreeMap()
    for num in nums:
        tree.add(num)
    return tree, set(nums)


def assert_empty(tree: TreeMap):
    assert len(tree) == 0, "empty tree should have length 0"
    assert tree.is_empty(), "empty tree should be marked as empty"
    assert tree.remove(5) is None, "removing from an empty tree should return None"
    for _ in tree:
        pytest.fail("iterating over an empty tree should not enter the loop")


def test_empty_tree():
    tree = TreeMap()
    assert_empty(tree)


def test_add_many_nums():
    nums = [5, 4, 7, 8, 4, 6, 2, 7, 1]
    tree = TreeMap()
    added = set()
    for num in nums:
        if num in added:
            assert not tree.add(num), "should return False to mark failed addition (duplicate)"
        else:
            assert tree.add(num), "should return True to mark a successful addition"
            added.add(num)
        assert len(tree) == len(added)
        assert list(tree) == sorted(added), \
            "iterating over tree should return numbers in order, and with no duplicates"


def test_remove_many_nums(tree_filled: Tuple[TreeMap, Set[int]]):
    tree, nums_original = tree_filled
    nums_remaining = list(nums_original)
    random.seed(42)
    random.shuffle(nums_remaining)
    bogus = max(nums_remaining) + 2
    while len(nums_remaining) > 0:
        num = nums_remaining[-1]
        del nums_remaining[-1]
        assert tree.remove(num) == num, "should return removed item to mark successful removal"
        assert len(tree) == len(nums_remaining)
        assert list(tree) == sorted(nums_remaining), \
            "iterating over tree should return numbers in order, and with no duplicates"
        assert tree.remove(bogus) is None, "should return None to mark failed removal"
    assert_empty(tree)
    for num in nums_original:
        assert tree.remove(num) is None, "should return None to mark failed removal"


def test_remove_root_nums(tree_filled: Tuple[TreeMap, Set[int]]):
    tree, nums_original = tree_filled
    nums_remaining = copy.copy(nums_original)
    while len(nums_remaining) > 0:
        to_remove = tree._root.value
        assert tree.remove(to_remove) == to_remove, \
            "should return removed item to mark successful removal"
        nums_remaining.remove(to_remove)
        assert len(tree) == len(nums_remaining)
        assert list(tree) == sorted(nums_remaining), \
            "iterating over tree should return numbers in order, and with no duplicates"
    assert_empty(tree)
    for num in nums_original:
        assert tree.remove(num) is None, "should return None to mark failed removal"


# TODO: tests about balance?
