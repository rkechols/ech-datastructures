from typing import List

import pytest

from ech_datastructures import TreeSet


@pytest.fixture(scope="function")
def nums() -> List[int]:
    return [5, 4, 7, 8, 4, 6, 2, 7, 1]


@pytest.fixture(scope="function")
def tree_filled(nums: List[int]) -> TreeSet[int]:
    return TreeSet(nums)


def assert_empty(tree: TreeSet):
    assert len(tree) == 0
    for _ in tree:
        pytest.fail("should not enter loop when iterating over empty TreeSet")
    # TODO


def test_empty_set():
    tree = TreeSet()
    assert_empty(tree)


def test_init(nums: List[int]):
    tree = TreeSet(nums)
    nums_set = set(nums)
    assert len(tree) == len(nums_set)
    assert list(tree) == sorted(nums_set)


def test_isdisjoint_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert tree1.isdisjoint(tree2)
    assert tree2.isdisjoint(tree1)


def test_isdisjoint_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert tree_empty.isdisjoint(tree_filled)
    assert tree_filled.isdisjoint(tree_empty)


def test_isdisjoint_positive():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert tree1.isdisjoint(tree2)
    assert tree2.isdisjoint(tree1)


def test_isdisjoint_negative():
    tree1 = TreeSet([1, 2, 3, 7])
    tree2 = TreeSet([6, 7, 8])
    assert not tree1.isdisjoint(tree2)
    assert not tree2.isdisjoint(tree1)


def test_issubset_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert tree1.issubset(tree2)
    assert tree2.issubset(tree1)


def test_issubset_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert tree_empty.issubset(tree_filled)
    assert not tree_filled.issubset(tree_empty)


def test_issubset_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert tree1.issubset(tree2)
    assert tree2.issubset(tree1)


def test_issubset_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert tree1.issubset(tree2)
    assert not tree2.issubset(tree1)


def test_issubset_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1.issubset(tree2)
    assert not tree2.issubset(tree1)


def test_issubset_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1.issubset(tree2)
    assert not tree2.issubset(tree1)


def test_issuperset_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert tree1.issuperset(tree2)
    assert tree2.issuperset(tree1)


def test_issuperset_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert not tree_empty.issuperset(tree_filled)
    assert tree_filled.issuperset(tree_empty)


def test_issuperset_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert tree1.issuperset(tree2)
    assert tree2.issuperset(tree1)


def test_issuperset_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1.issuperset(tree2)
    assert tree2.issuperset(tree1)


def test_issuperset_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1.issuperset(tree2)
    assert not tree2.issuperset(tree1)


def test_issuperset_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1.issuperset(tree2)
    assert not tree2.issuperset(tree1)
