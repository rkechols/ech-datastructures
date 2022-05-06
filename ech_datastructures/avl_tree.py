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

    def find(self, item: T, item_key: Any = None) -> Optional["_AVLTreeNode"]:
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # found it!
            return self
        elif item_key < self_key:
            # go left (if we can)
            if self.left is None:
                return None  # dead end
            return self.left.find(item, item_key)
        else:  # item_key > self_key
            # go right (if we can)
            if self.right is None:
                return None  # dead end
            return self.right.find(item, item_key)

    def __iter__(self) -> Generator["_AVLTreeNode[T]", None, None]:
        if self.left is not None:
            for descendant in self.left:
                yield descendant
        yield self
        if self.right is not None:
            for descendant in self.right:
                yield descendant

    def add(self, item: T, item_key: Any) -> bool:
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # duplicate
            return False
        elif item_key < self_key:
            if self.left is None:
                # found the spot to add it
                self.left = _AVLTreeNode(item, parent=self, key=self._key)
                return True
            # keep walking
            return self.left.add(item, item_key)
        else:  # item_key > self_key
            if self.right is None:
                # found the spot to add it
                self.right = _AVLTreeNode(item, parent=self, key=self._key)
                return True
            # keep walking
            return self.right.add(item, item_key)

    def remove(self, item: T, item_key: Any) -> bool:
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # found it!
            # TODO
            raise NotImplementedError(self.value)
        elif item_key < self_key:
            if self.left is None:
                # dead end
                return False
            # keep walking
            return self.left.remove(item, item_key)
        else:  # item_key > self_key
            if self.right is None:
                # dead end
                return False
            # keep walking
            return self.right.remove(item, item_key)

    def __repr__(self) -> str:
        return f"_AVLTreeNode({self.value})"


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

    def add(self, item: T) -> bool:
        if self._root is None:
            self._root = _AVLTreeNode(item, key=self._key)
            success = True
        else:
            success = self._root.add(item, self._key(item))
        if success:
            self._count += 1
        return success

    def remove(self, item: T) -> bool:
        if self._root is None:
            # nothing to remove
            return False
        # we need to check if we're removing the root
        item_key = self._key(item)
        root_key = self._key(self._root)
        # removing the root is special if it has no children
        if item_key == root_key and self._root.left is None and self._root.right is None:
            self._root = None
            success = True
        else:  # not any special situation
            success = self._root.remove(item, item_key)
        if success:
            self._count -= 1
        return success

    # TODO: bulk operations? https://en.wikipedia.org/wiki/AVL_tree#:~:text=log%20n)%20time.-,Set%20operations%20and%20bulk%20operations,-%5Bedit%5D

    def __len__(self) -> int:
        """
        Check the number of elements in the AVLTree.

        Returns
        -------
        int - number of elements in the AVLTree.
        """
        return self._count

    def is_empty(self) -> bool:
        """
        Check if the AVLTree is empty or not.

        Returns
        -------
        bool - `True` if there is no data in the AVLTree, `False` otherwise.
        """
        return self.__len__() == 0

    def clear(self):
        """
        Empty all data from the AVLTree.

        Returns
        -------
        None
        """
        self._root = None
        self._count = 0
