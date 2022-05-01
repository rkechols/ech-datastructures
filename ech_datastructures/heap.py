import heapq
from typing import Any, Callable, Generic, Iterable, TypeVar, List


T = TypeVar("T")


class _HeapElem(Generic[T]):
    __slots__ = "val", "key"

    def __init__(self, val: T, key: Callable[[T], Any]):
        self.val = val
        self.key = key

    def __lt__(self, other: "_HeapElem[T]") -> bool:
        return self.key(self.val) < self.key(other.val)


class Heap(Generic[T]):
    __slots__ = "_data", "_key"

    def __init__(self, data: Iterable[T] = None, key: Callable[[T], Any] = None):
        # save provided sorting key, if any
        if key is None:
            self._key = lambda x: x
        else:
            self._key = key
        # save provided data, if any
        if data is None:
            self._data = []
        else:
            self._data = [_HeapElem(x, key=self._key) for x in data]
            heapq.heapify(self._data)

    @property
    def data(self) -> List[T]:
        return [elem.val for elem in self._data]

    def peek(self) -> T:
        try:
            return self._data[0].val
        except IndexError as e:
            raise IndexError("peek from empty Heap") from e

    def pop(self) -> T:
        try:
            return heapq.heappop(self._data).val
        except IndexError as e:
            raise IndexError("pop from empty Heap") from e

    def add(self, new_item: T):
        heapq.heappush(self._data, _HeapElem(new_item, key=self._key))

    def add_pop(self, new_item: T) -> T:
        return heapq.heappushpop(self._data, _HeapElem(new_item, key=self._key)).val

    def pop_add(self, new_item: T) -> T:
        try:
            return heapq.heapreplace(self._data, _HeapElem(new_item, key=self._key)).val
        except IndexError as e:
            raise IndexError("pop_add from empty Heap") from e

    def update(self, new_items: Iterable[T]):
        for item in new_items:
            self.add(item)

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return self.__len__() == 0

    def clear(self):
        self._data.clear()
