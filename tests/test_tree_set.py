import random
from typing import List, Set

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
    for x in tree:
        pytest.fail(f"should not enter loop when iterating over empty TreeSet ({x})")
    with pytest.raises(KeyError):
        tree.remove(5)
    with pytest.raises(KeyError):
        tree.pop()


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


def test_le_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert tree1 <= tree2
    assert tree2 <= tree1


def test_le_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert tree_empty <= tree_filled
    assert not tree_filled <= tree_empty


def test_le_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert tree1 <= tree2
    assert tree2 <= tree1


def test_le_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert tree1 <= tree2
    assert not tree2 <= tree1


def test_le_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 <= tree2
    assert not tree2 <= tree1


def test_le_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1 <= tree2
    assert not tree2 <= tree1


def test_lt_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert not tree1 < tree2
    assert not tree2 < tree1


def test_lt_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert tree_empty < tree_filled
    assert not tree_filled < tree_empty


def test_lt_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert not tree1 < tree2
    assert not tree2 < tree1


def test_lt_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert tree1 < tree2
    assert not tree2 < tree1


def test_lt_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 < tree2
    assert not tree2 < tree1


def test_lt_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1 < tree2
    assert not tree2 < tree1


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


def test_ge_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert tree1 >= tree2
    assert tree2 >= tree1


def test_ge_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert not tree_empty >= tree_filled
    assert tree_filled >= tree_empty


def test_ge_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert tree1 >= tree2
    assert tree2 >= tree1


def test_ge_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 >= tree2
    assert tree2 >= tree1


def test_ge_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 >= tree2
    assert not tree2 >= tree1


def test_ge_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1 >= tree2
    assert not tree2 >= tree1


def test_gt_both_empty():
    tree1 = TreeSet()
    tree2 = TreeSet()
    assert not tree1 > tree2
    assert not tree2 > tree1


def test_gt_one_empty(tree_filled: TreeSet[int]):
    tree_empty = TreeSet()
    assert not tree_empty > tree_filled
    assert tree_filled > tree_empty


def test_gt_equal(nums: List[int]):
    tree1 = TreeSet(nums)
    tree2 = TreeSet(nums)
    assert not tree1 > tree2
    assert not tree2 > tree1


def test_gt_positive():
    tree1 = TreeSet([3, 4, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 > tree2
    assert tree2 > tree1


def test_gt_negative_overlap():
    tree1 = TreeSet([2, 3, 4, 5, 7, 8])
    tree2 = TreeSet([1, 3, 4, 6, 7, 8, 9])
    assert not tree1 > tree2
    assert not tree2 > tree1


def test_gt_negative_disjoint():
    tree1 = TreeSet([1, 2, 3])
    tree2 = TreeSet([5, 6, 7, 8])
    assert not tree1 > tree2
    assert not tree2 > tree1


# TODO: more tests


def test_xor_positive():
    tree1 = TreeSet([3, 4, 7, 8, 9])
    tree2 = TreeSet([1, 2, 4, 6, 7, 9])
    result = list(tree1 ^ tree2)
    assert result == list(tree2 ^ tree1)
    assert result == [1, 2, 3, 6, 8]


# TODO: more tests


def assert_equivalence(tree: TreeSet, hash_set: Set):
    assert list(tree) == sorted(hash_set)


def test_random_set_parity():
    random.seed(42)
    n_trials = 500
    options = list(range(10))
    for trial_num in range(n_trials):
        starters = random.sample(options, k=random.randrange(10))
        tree = TreeSet(starters)
        hash_set = set(starters)
        assert_equivalence(tree, hash_set)
        for step_num in range(random.randrange(5, 20)):
            val = random.choice(options)
            if random.random() < 0.5:
                tree.add(val)
                hash_set.add(val)
            else:
                tree.discard(val)
                hash_set.discard(val)
            assert_equivalence(tree, hash_set)
        for _ in range(len(tree)):
            removed = tree.pop()
            hash_set.remove(removed)
            assert_equivalence(tree, hash_set)
        assert_empty(tree)
