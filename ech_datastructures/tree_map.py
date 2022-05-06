from typing import Any, Generic, Iterable, Tuple, TypeVar, Union, Mapping


K = TypeVar("K")
V = TypeVar("V")


class TreeMap(Generic[K, V]):
    def __init__(self):
        pass

    def clear(self):
        # TODO
        raise NotImplementedError

    def get(self, k: K, default: V = None) -> V:
        # TODO
        raise NotImplementedError

    def items(self) -> Iterable[Tuple[K, V]]:
        # TODO
        raise NotImplementedError

    def keys(self) -> Iterable[K]:
        # TODO
        raise NotImplementedError

    def values(self) -> Iterable[V]:
        # TODO
        raise NotImplementedError

    def pop(self, k: K, default: V = None) -> V:
        # TODO
        raise NotImplementedError

    def popitem(self) -> Tuple[K, V]:
        # TODO
        raise NotImplementedError

    # def setdefault

    def update(self, new_pairs: Union[Mapping[K, V], Iterable[Tuple[K, V]]], **kwargs):
        # TODO
        raise NotImplementedError

    def __contains__(self, k: K) -> bool:
        # TODO
        raise NotImplementedError

    def __delitem__(self, k: K):
        # TODO
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        # TODO
        raise NotImplementedError

    def __getitem__(self, k: K) -> V:
        # TODO
        raise NotImplementedError

    def __iter__(self):
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO
        raise NotImplementedError

    def __ne__(self, other: Any) -> bool:
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO
        raise NotImplementedError

    __hash__ = None
