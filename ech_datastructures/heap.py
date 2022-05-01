import heapq
from typing import Any, Callable, Generic, Iterable, TypeVar


T = TypeVar("T")


class Heap(Generic[T]):
    __slots__ = "_data", "_key"

    def __init__(self, data: Iterable[T] = None, key: Callable[[T], Any] = None):
        # save provided data, if any
        if data is None:
            self._data = []
        else:
            self._data = [x for x in data]
            heapq.heapify(self._data)
        # save provided sorting key, if any
        if key is None:
            self._key = lambda x: x
        else:
            self._key = key

    def peek(self) -> T:
        # TODO
        raise NotImplementedError

    def pop(self) -> T:
        # TODO
        raise NotImplementedError

    def add(self, new_item: T):
        # TODO
        raise NotImplementedError

    def pop_add(self, new_item: T) -> T:
        # TODO
        raise NotImplementedError

    def update(self, new_items: Iterable[T]):
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return self.__len__() == 0

    def clear(self):
        self._data.clear()
