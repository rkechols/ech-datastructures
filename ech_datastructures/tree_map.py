from collections.abc import Iterable as IterableABC, Mapping as MappingABC
from itertools import chain
from typing import Any, Generator, Generic, Iterable, List, Mapping, Tuple, TypeVar, Union

from ech_datastructures.avl_tree import AVLTree


K = TypeVar("K")
V = TypeVar("V")


class _TreeMapNode(Generic[K, V]):
    def __init__(self, k: K, v: V):
        self.k = k
        self.v = v

    @staticmethod
    def key(node: "_TreeMapNode[K, V]") -> K:
        return node.k


class TreeMap(MappingABC, Generic[K, V]):
    __slots__ = ("_tree",)  # tuple, length 1

    def __init__(self):
        self._tree: AVLTree[_TreeMapNode[K, V]] = AVLTree(key=_TreeMapNode.key)

    def clear(self):
        self._tree.clear()

    def get(self, key: K, default: V = None) -> V:
        result = self._tree.find(key)
        if result is None:
            if default is None:
                raise KeyError(key)
            # else:
            return default
        return result.v

    def items(self) -> List[Tuple[K, V]]:
        to_return = []
        for node in self._tree:
            to_return.append((node.k, node.v))
        return to_return

    def keys(self) -> List[K]:
        to_return = []
        for node in self._tree:
            to_return.append(node.k)
        return to_return

    def values(self) -> List[V]:
        to_return = []
        for node in self._tree:
            to_return.append(node.v)
        return to_return

    def pop(self, k: K, default: V = None) -> V:
        result = self._tree.remove(k)
        if result is None:
            if default is None:
                raise KeyError(k)
            # else:
            return default
        return result.v

    def popitem(self) -> Tuple[K, V]:
        if len(self._tree) == 0:
            raise KeyError("map is empty")
        # what key to pop?
        k = next(iter(self._tree)).k
        # pop it
        result = self._tree.remove(k)
        return result.k, result.v

    def setdefault(self, k: K, default: V = None) -> V:
        result = self._tree.find(k)
        if result is None:
            self._tree.add(_TreeMapNode(k, default))
            return default
        return result.v

    def update(self, new_pairs: Union[Mapping[K, V], Iterable[Tuple[K, V]]], **kwargs):
        if isinstance(new_pairs, MappingABC):
            tup_iter = new_pairs.items()
        elif isinstance(new_pairs, IterableABC):
            tup_iter = new_pairs
        else:
            raise TypeError(f"`new_pairs` must be a Mapping or Iterable "
                            f"(actual class is {new_pairs.__class__})")
        for k, v in chain(tup_iter, kwargs.items()):
            self._tree.add(_TreeMapNode(k, v), overwrite=True)

    def __contains__(self, k: K) -> bool:
        return k in self._tree

    def __delitem__(self, k: K):
        result = self._tree.remove(k)
        if result is None:
            raise KeyError(k)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if len(self) != len(other):
            return False
        for self_node, other_node in zip(self._tree, other._tree):
            if self_node.k != other_node.k:
                return False
            if self_node.v != other_node.v:
                return False
        return True

    def __getitem__(self, k: K) -> V:
        result = self._tree.find(k)
        if result is None:
            raise KeyError(k)
        return result.v

    def __setitem__(self, k: K, v: V):
        self._tree.add(_TreeMapNode(k, v), overwrite=True)

    def __iter__(self) -> Generator[K, None, None]:
        for node in self._tree:
            yield node.k

    def __len__(self) -> int:
        return len(self._tree)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(len={self.__len__()})"

    __hash__ = None
