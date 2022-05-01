import copy
from collections import Counter
from typing import Sequence

import pytest

from ech_datastructures import Heap


def assert_empty(h: Heap):
    assert len(h) == 0, "empty heap should have length 0"
    assert h.is_empty(), "empty heap should be marked as empty"
    with pytest.raises(IndexError):
        h.peek()
    with pytest.raises(IndexError):
        h.pop()
    with pytest.raises(IndexError):
        h.pop_add(5)


def test_empty_heap():
    h = Heap()
    assert_empty(h)


def _heapify_pop_all(vals: Sequence):
    vals_copy = copy.copy(vals)
    h = Heap(vals)
    assert vals == vals_copy, "making a heap from a list should not change the original list"
    count_original = Counter(vals)
    count_heap = Counter(h._data)
    assert count_original == count_heap, "the heap does not have the same elements as the original list"
    pop_order = []
    n_remaining = len(vals)
    while not h.is_empty():
        pop_order.append(h.pop())
        n_remaining -= 1
        assert len(h) == n_remaining, "while popping all in succession, the heap size was not decreasing by one"
    assert pop_order == sorted(vals), "values did not pop in the correct order"
    assert_empty(h)


def test_heapify_pop_all_ints():
    nums = [5, 4, 7, 8, 4, 6, 2, 7, 1]
    _heapify_pop_all(nums)


def test_heapify_pop_all_strings():
    words = ["potato", "zoological", "alphabet", "MEGALODON", "uNStAbLE", "alphabet", "Spider-Man", "white space"]
    _heapify_pop_all(words)


def test_heapify_pop_all_letters():
    letters = "qwertyABRACADABRA--quick brown fox"
    _heapify_pop_all(letters)


def test_heapify_pop_all_reverse():
    vals = [5, 4, 7, 8, 4, 6, 2, 7, 1]
    vals_copy = copy.copy(vals)
    h = Heap(vals, key=lambda x: -1 * x)
    assert vals == vals_copy, "making a heap from a list should not change the original list"
    pop_order = []
    while not h.is_empty():
        pop_order.append(h.pop())
    assert pop_order == sorted(vals, reverse=True), "values did not pop in the correct order"
    assert_empty(h)


def test_update_pop_all():
    vals = [5, 4, 7, 8, 4, 6, 2, 7, 1]
    h = Heap(vals)
    assert len(h) == len(vals)
    vals2 = [5, 6, 4, 7, 2, 2, 0]
    h.update(vals2)
    joined = vals + vals2
    assert len(h) == len(joined)
    count_joined = Counter(joined)
    count_heap = Counter(h._data)
    assert count_joined == count_heap, "the updated heap does not have the same elements as the joined list"
    pop_order = []
    while not h.is_empty():
        pop_order.append(h.pop())
    assert pop_order == sorted(joined), "values did not pop in the correct order"
    assert_empty(h)


# TODO: test peek, add, pop_add, clear
