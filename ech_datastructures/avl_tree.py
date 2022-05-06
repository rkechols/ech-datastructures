from typing import Any, Generic, Optional, TypeVar, Callable, Generator


T = TypeVar("T")


class _AVLTreeNode(Generic[T]):
    __slots__ = "value", "left", "right", "parent", "_key"

    def __init__(self,
                 value: T,
                 *,
                 left: "_AVLTreeNode[T]" = None,
                 right: "_AVLTreeNode[T]" = None,
                 parent: "_AVLTreeNode[T]" = None,
                 key: Callable[[T], Any]):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self._key = key

    def find(self, item: T) -> Optional["_AVLTreeNode"]:
        item_key = self._key(item)
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # found it!
            return self
        elif item_key < self_key:
            # go left (if we can)
            if self.left is None:
                return None  # dead end
            return self.left.find(item)
        else:  # item_key > self_key
            # go right (if we can)
            if self.right is None:
                return None  # dead end
            return self.right.find(item)

    def __iter__(self) -> Generator["_AVLTreeNode[T]", None, None]:
        if self.left is not None:
            for descendant in self.left:
                yield descendant
        yield self
        if self.right is not None:
            for descendant in self.right:
                yield descendant


class AVLTree(Generic[T]):
    __slots__ = "_key", "_root", "_count"

    def __init__(self, key: Callable[[T], Any] = None):
        self._key = key if key is not None else lambda x: x  # by default just use the value itself
        self._root: Optional[_AVLTreeNode[T]] = None
        self._count = 0

    def __contains__(self, item: T) -> bool:
        if self._root is None:
            return False
        return self._find(item) is not None

    def _find(self, item: T) -> Optional["_AVLTreeNode"]:
        if self._root is None:
            return None
        return self._root.find(item)

    def __iter__(self) -> Generator[T, None, None]:
        if self._root is None:
            return
        for descendant in self._root:
            yield descendant.value
