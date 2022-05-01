from ech_datastructures import Heap
import pytest


def test_empty_heap():
    h = Heap()
    assert len(h) == 0, "empty heap should have length 0"
    assert h.is_empty(), "empty heap should be marked as empty"
    with pytest.raises(IndexError):
        h.peek()
    with pytest.raises(IndexError):
        h.pop()
    with pytest.raises(IndexError):
        h.pop_add(5)
