from typing import Any, Generic, Optional, TypeVar, Callable, Generator


T = TypeVar("T")


class _AVLTreeNode(Generic[T]):
    __slots__ = "value", "left", "right", "parent"

    def __init__(self,
                 value: T,
                 *,
                 left: "_AVLTreeNode[T]" = None,
                 right: "_AVLTreeNode[T]" = None,
                 parent: "_AVLTreeNode[T]" = None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

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
        item_key = self._key(item)
        current = self._root
        while current is not None:
            # do a comparison against the current node
            self_key = self._key(current.value)
            if item_key == self_key:
                # found it!
                return current
            elif item_key < self_key:
                # "less than" means left
                current = current.left
            else:  # item_key > self_key
                # "greater than" means right
                current = current.right
        # dead end
        return None

    def __iter__(self) -> Generator[T, None, None]:
        if self._root is None:
            return
        # go all the way to the left
        for descendant in self._root:
            yield descendant.value
