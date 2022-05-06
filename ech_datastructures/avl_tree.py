from typing import Any, Generic, Optional, TypeVar, Callable


T = TypeVar("T")


class _AVLTreeNode(Generic[T]):
    __slots__ = "value", "left", "right", "_key"

    def __init__(self,
                 value: T,
                 *,
                 left: "_AVLTreeNode" = None,
                 right: "_AVLTreeNode" = None):
        self.value = value
        self.left = left
        self.right = right


class AVLTree(Generic[T]):
    def __init__(self, key: Callable[[T], Any] = None):
        self._key = key if key is not None else lambda x: x  # by default just use the value itself
        self._root: Optional[_AVLTreeNode[T]] = None
        self._count = 0

    def __contains__(self, item: T) -> bool:
        if self._root is None:
            return False
        return self._root.find(item) is not None

    def find(self, item: T) -> Optional["_AVLTreeNode"]:
        # is it here?
        item_key = self._key(item)
        self_key = self._key(self.value)
        if item_key == self_key:
            return self
        elif item_key < self_key:
            if self.left is None:
                return None
            else:
                return self.left.find(item)
        else:  # item_key > self_key
            if self.right is None:
                return None
            else:
                return self.right.find(item)
