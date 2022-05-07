from typing import Any, Generic, Iterable, List, Mapping, Tuple, TypeVar, Union

from .avl_tree import AVLTree


K = TypeVar("K")
V = TypeVar("V")


class _TreeMapNode(Generic[K, V]):
    def __init__(self, k: K, v: V):
        self.k = k
        self.v = v

    @staticmethod
    def key(node: "_TreeMapNode[K, V]") -> K:
        return node.k


class TreeMap(Generic[K, V]):
    __slots__ = "_tree",  # comma makes it a tuple, like it needs to be

    def __init__(self):
        self._tree: AVLTree[_TreeMapNode[K, V]] = AVLTree(key=_TreeMapNode.key)

    def clear(self):
        self._tree.clear()

    def get(self, k: K, default: V = None) -> V:
        result = self._tree.find_by_key(k)
        if result is None:
            if default is None:
                raise KeyError(k)
            else:
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
        return len(self._tree)

    def __ne__(self, other: Any) -> bool:
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO
        raise NotImplementedError

    __hash__ = None
