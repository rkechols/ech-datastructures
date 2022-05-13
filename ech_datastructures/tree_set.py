from typing import Any, Generator, Generic, Iterable, TypeVar

from ech_datastructures.tree_map import TreeMap


T = TypeVar("T")


def _subset_check(subset_candidate: Iterable[T], superset_candidate: Iterable[T]) -> bool:
    # by contract, both `self` and `other` are sorted and non-empty
    iter_other = iter(superset_candidate)
    curr_other = next(iter_other)
    for curr_self in subset_candidate:
        while True:
            if curr_other < curr_self:
                try:
                    curr_other = next(iter_other)
                except StopIteration:
                    # got to the end without finding curr_self
                    return False
            elif curr_other == curr_self:
                # found it!
                break  # break the while, go on to the next `curr_self`
            else:  # curr_other > curr_self:
                # we missed it
                return False
    # all were found
    return True


class TreeSet(Generic[T]):
    def __init__(self, data: Iterable[T] = None):
        self._map: TreeMap[T, None] = TreeMap()
        # add any starter data
        if data is not None:
            for elem in data:
                self._map[elem] = None

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, item: T) -> bool:
        return item in self._map

    def __iter__(self) -> Generator[T, None, None]:
        for item in self._map:
            yield item

    def isdisjoint(self, other: "TreeSet[T]") -> bool:
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        if self.__len__() == 0 or len(other) == 0:
            return True
        # zipper iterate
        iter_self = iter(self)
        iter_other = iter(other)
        curr_self = next(iter_self)
        curr_other = next(iter_other)
        while True:
            if curr_self == curr_other:
                # found overlap; bad
                return False
            try:
                if curr_self > curr_other:
                    curr_other = next(iter_other)
                else:  # curr_self < curr_other
                    curr_self = next(iter_self)
            except StopIteration:
                # one ran out
                return True

    def issubset(self, other: Iterable[T]) -> bool:
        if self.__len__() == 0:
            return True
        other = list(other)
        n = len(other)
        if n == 0:
            # at this point in the code, we know `self` is non-empty,
            # so all of its elements are missing from `other`
            return False
        other.sort()
        return _subset_check(self, other)

    def __le__(self, other: "TreeSet[T]") -> bool:
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        if self.__len__() == 0:
            return True
        if len(other) == 0:
            return False
        return _subset_check(self, other)

    def __lt__(self, other: "TreeSet[T]") -> bool:
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        is_subset = self.__le__(other)
        return is_subset and self.__len__() < len(other)

    def issuperset(self, other: Iterable[T]) -> bool:
        other = list(other)
        n = len(other)
        if n == 0:
            return True
        if self.__len__() == 0:
            # at this point in the code, we know `other` is non-empty,
            # so all of its elements are missing from `self`
            return False
        other.sort()
        return _subset_check(other, self)

    def __ge__(self, other: "TreeSet[T]") -> bool:
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        if len(other) == 0:
            return True
        if self.__len__() == 0:
            return False
        return _subset_check(other, self)

    def __gt__(self, other: "TreeSet[T]") -> bool:
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        is_superset = self.__ge__(other)
        return is_superset and len(other) < self.__len__()

    def union(self, *others: Iterable[Iterable[T]]) -> "TreeSet[T]":
        # TODO
        raise NotImplementedError

    def __or__(self, other: "TreeSet[T]") -> "TreeSet[T]":
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def intersection(self, *others: Iterable[Iterable[T]]) -> "TreeSet[T]":
        # TODO
        raise NotImplementedError

    def __and__(self, other: "TreeSet[T]") -> "TreeSet[T]":
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def difference(self, *others: Iterable[Iterable[T]]) -> "TreeSet[T]":
        # TODO
        raise NotImplementedError

    def __sub__(self, other: "TreeSet[T]") -> "TreeSet[T]":
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def symmetric_difference(self, other: Iterable[T]) -> "TreeSet[T]":
        # TODO
        raise NotImplementedError

    def __xor__(self, other: "TreeSet[T]") -> "TreeSet[T]":
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def copy(self) -> "TreeSet[T]":
        # TODO
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TreeSet):
            return False
        # TODO
        raise NotImplementedError

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def update(self, *others: Iterable[Iterable[T]]):
        # TODO
        raise NotImplementedError

    def __ior__(self, other: "TreeSet[T]"):
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def intersection_update(self, *others: Iterable[Iterable[T]]):
        # TODO
        raise NotImplementedError

    def __iand__(self, other: "TreeSet[T]"):
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def difference_update(self, *others: Iterable[Iterable[T]]):
        # TODO
        raise NotImplementedError

    def __isub__(self, other: "TreeSet[T]"):
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def symmetric_difference_update(self, other: Iterable[T]):
        # TODO
        raise NotImplementedError

    def __ixor__(self, other: "TreeSet[T]"):
        if not isinstance(other, TreeSet):
            raise ValueError(f"`other` must be a TreeSet, but was {other.__class__.__name__}")
        # TODO
        raise NotImplementedError

    def add(self, elem: T):
        # TODO
        raise NotImplementedError

    def remove(self, elem: T):
        # TODO
        raise NotImplementedError

    def discard(self, elem: T):
        # TODO
        raise NotImplementedError

    def pop(self) -> T:
        # TODO
        raise NotImplementedError

    def clear(self):
        # TODO
        raise NotImplementedError

    __hash__ = None
