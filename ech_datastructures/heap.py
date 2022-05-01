import heapq
from typing import Any, Callable, Iterable, TypeVar, Generic


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
        pass  # TODO

    def pop(self) -> T:
        pass  # TODO

    def add(self, new_item: T):
        pass  # TODO

    def pop_add(self, new_item: T) -> T:
        pass  # TODO

    def update(self, new_items: Iterable[T]):
        pass  # TODO

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return self.__len__() == 0

    def clear(self):
        self._data.clear()
