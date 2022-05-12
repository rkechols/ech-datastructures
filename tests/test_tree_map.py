import copy
import random
from typing import List, Set, Tuple

import pytest

from ech_datastructures import TreeMap


NUM_MAP = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE"
}


@pytest.fixture(scope="function")
def nums() -> List[Tuple[int, str]]:
    return [(x, NUM_MAP[x]) for x in [5, 4, 7, 8, 6, 2, 1]]


@pytest.fixture(scope="function")
def tree_filled(nums: List[Tuple[int, str]]) -> Tuple[TreeMap, Set[int]]:
    tree = TreeMap()
    nums_set = set()
    for num, num_str in nums:
        tree[num] = num_str
        nums_set.add(num)
    return tree, nums_set


def assert_empty(tree: TreeMap):
    assert len(tree) == 0, "empty tree should have length 0"
    with pytest.raises(KeyError):
        del tree[1]
    with pytest.raises(KeyError):
        print(tree[2])
    assert 3 not in tree, "empty tree should have no contents"
    with pytest.raises(KeyError):
        tree.pop(4)
    assert tree.get(5, "potato") == "potato"
    assert len(list(tree.items())) == 0
    with pytest.raises(KeyError):
        tree.popitem()
    for _ in tree:
        pytest.fail("iterating over an empty tree should not enter the loop")


def test_empty_tree():
    tree = TreeMap()
    assert_empty(tree)


def test_add_many_nums():
    nums = [(x, NUM_MAP[x]) for x in [5, 4, 7, 8, 6, 2, 1]]
    tree = TreeMap()
    added = set()
    for num, num_str in nums:
        tree[num] = num_str
        added.add(num)
        assert len(tree) == len(added)
        added_list = sorted(added)
        assert list(tree.keys()) == added_list, \
            "iterating over tree should return numbers in order, and with no duplicates"
        assert list(tree.values()) == [NUM_MAP[x] for x in added_list]


def test_remove_many_nums(tree_filled: Tuple[TreeMap, Set[int]]):
    tree, nums_original = tree_filled
    nums_remaining = list(nums_original)
    random.seed(42)
    random.shuffle(nums_remaining)
    bogus = max(nums_remaining) + 2
    while len(nums_remaining) > 0:
        num = nums_remaining[-1]
        del nums_remaining[-1]
        assert tree.pop(num) == NUM_MAP[num], "should return removed item to mark successful removal"
        assert len(tree) == len(nums_remaining)
        assert list(tree) == sorted(nums_remaining), \
            "iterating over tree should return numbers in order, and with no duplicates"
        assert tree.pop(bogus, default="potato") == "potato", "should return None to mark failed removal"
    assert_empty(tree)
    for num in nums_original:
        assert tree.pop(num, default="potato2") == "potato2", "should return None to mark failed removal"


def test_remove_root_nums(tree_filled: Tuple[TreeMap, Set[int]]):
    tree, nums_original = tree_filled
    nums_remaining = copy.copy(nums_original)
    while len(nums_remaining) > 0:
        k, v = tree.popitem()
        nums_remaining.remove(k)
        assert len(tree) == len(nums_remaining)
        assert list(tree) == sorted(nums_remaining), \
            "iterating over tree should return numbers in order, and with no duplicates"
    assert_empty(tree)


# TODO: tests about balance?
