from typing import Any, Callable, Generator, Generic, Optional, TypeVar


T = TypeVar("T")


class _AVLTreeNode(Generic[T]):
    """
    Intended only as a "helper class" to AVLTree.
    Stores a single value, as well as connections that define the tree structure.
    """
    __slots__ = "value", "left", "right", "parent", "_key"

    def __init__(self,
                 value: T,
                 *,
                 left: "_AVLTreeNode[T]" = None,
                 right: "_AVLTreeNode[T]" = None,
                 parent: "_AVLTreeNode[T]" = None,
                 key: Callable[[T], Any]):
        """
        Construct a node of a self-balancing binary tree.

        Parameters
        ----------
        value: T - the value to be stored in this node
        left: _AVLTreeNode[T] - the left child of this node, by default None
        right: _AVLTreeNode[T] - the right child of this node, by default None
        parent: _AVLTreeNode[T] - the parent of this node, by default None
        key: Callable[[T], Any] - a function to convert a stored item to
            a comparable value. The return values of this function determine
            ordering and equality of elements.
            By default, None
            If None, the identity function `lambda x: x` is used, meaning
            elements are compared directly.
        """
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self._key = key

    def find(self, item: T, item_key: Any) -> Optional["_AVLTreeNode"]:
        """
        Retrieve the node with the given value, if present in the subtree starting at this node.

        Parameters
        ----------
        item: T - the value to find
        item_key: Any - the precalculated key value of `item`
            passed for computational efficiency.

        Returns
        -------
        Optional[_AVLTreeNode] - the node containing the value
            None if the value is not present
        """
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # found it!
            return self
        if item_key < self_key:
            # go left (if we can)
            if self.left is None:
                return None  # dead end
            return self.left.find(item, item_key)
        # else:  # item_key > self_key
        # go right (if we can)
        if self.right is None:
            return None  # dead end
        return self.right.find(item, item_key)

    def __iter__(self) -> Generator["_AVLTreeNode[T]", None, None]:
        """
        Iterate over the subtree starting at this node, in order from least to greatest

        Returns
        -------
        Generator[_AVLTreeNode[T], None, None] - lazily generates the nodes from least to greatest
        """
        if self.left is not None:
            for descendant in self.left:
                yield descendant
        yield self
        if self.right is not None:
            for descendant in self.right:
                yield descendant

    def add(self, item: T, item_key: Any) -> bool:
        """
        Add a value to the subtree starting at this node, if not already present

        Parameters
        ----------
        item: T - the value to try to add
        item_key: Any - the precalculated key value of `item`
            passed for computational efficiency

        Returns
        -------
        bool - if the addition was successful or not
            True if the value was added
            False if the value was already present
        """
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # duplicate
            return False
        if item_key < self_key:
            if self.left is None:
                # found the spot to add it
                self.left = _AVLTreeNode(item, parent=self, key=self._key)
                return True
            # keep walking
            return self.left.add(item, item_key)
        # else:  # item_key > self_key
        if self.right is None:
            # found the spot to add it
            self.right = _AVLTreeNode(item, parent=self, key=self._key)
            return True
        # keep walking
        return self.right.add(item, item_key)

    # pylint: disable=too-many-branches
    def remove(self, item: T, item_key: Any) -> bool:
        """
        Remove a value from the subtree that starts at this node, if present

        Parameters
        ----------
        item: T - the value to try to remove
        item_key: Any - the precalculated key value of `item`
            passed for computational efficiency

        Returns
        -------
        bool - if the removal was successful or not
            True if the value was found and remove
            False if the value was not present
        """
        self_key = self._key(self.value)
        # compare the keys
        if item_key == self_key:
            # found it!
            if self.left is None:
                # re-point the parent to the right child of this one
                if self.parent.left is self:
                    self.parent.left = self.right
                else:  # self.parent.right is self:
                    self.parent.right = self.right
                # re-point the right child of this one to its new parent
                if self.right is not None:
                    self.right.parent = self.parent
                # even though `self` has outdated pointers, nothing now points to it
            # self.left is not None
            elif self.right is None:
                # re-point the parent to the left child of this one
                if self.parent.left is self:
                    self.parent.left = self.left
                else:  # self.parent.right is self
                    self.parent.right = self.left
                # re-point the left child of this one to its new parent
                if self.left is not None:
                    self.left.parent = self.parent
                # even though `self` has outdated pointers, nothing now points to it
                return True
            # neither self.left nor self.right is None
            else:
                # go find the "in-order predecessor
                current = self.left
                while current.right is not None:
                    current = current.right
                # put its value into the current one
                self.value = current.value
                # remove the lower one
                current.remove(current.value, self._key(current.value))
                # even thought that call to current.remove is recursive,
                # we know it's already at the node it needs to remove,
                # and that that node has no right child,
                # so it will not recurse again
            return True
        if item_key < self_key:
            if self.left is None:
                # dead end
                return False
            # keep walking
            return self.left.remove(item, item_key)
        # else:  # item_key > self_key
        if self.right is None:
            # dead end
            return False
        # keep walking
        return self.right.remove(item, item_key)

    def __repr__(self) -> str:
        """
        Give a string representation of the node.
        For debugging purposes.

        Returns
        -------
        str - a simple string value to represent the node
        """
        return f"_AVLTreeNode({self.value})"


class AVLTree(Generic[T]):  # TODO: actually add the balancing part
    """
    A self-balancing binary tree.

    Does not allow duplicate values.

    Order and equality of elements is determined by the return values of
    the `key` function.

    `T` represents the type of items being stored in the Heap.
    """
    __slots__ = "_key", "_root", "_count"

    def __init__(self, key: Callable[[T], Any] = None):
        """
        Construct an AVLTree.

        Parameters
        ----------
        key: Callable[[T], Any] - a function to convert a stored item to
            a comparable value. The return values of this function determine
            ordering and equality of elements.
            By default, None
            If None, the identity function `lambda x: x` is used, meaning
            elements are compared directly.
        """
        self._key = key if key is not None else lambda x: x  # by default just use the value itself
        self._root: Optional[_AVLTreeNode[T]] = None
        self._count = 0

    def __contains__(self, item: T) -> bool:
        """
        check if the value is present in the tree

        Parameters
        ----------
        item: T - the value to search for

        Returns
        -------
        bool - if the value is present or not
            True if the value is in the tree
            False if the value is not in the tree
        """
        if self._root is None:
            return False
        return self._find(item) is not None

    def _find(self, item: T) -> Optional["_AVLTreeNode"]:
        """
        Helper function to retrieve the node with the given value, if present.

        Parameters
        ----------
        item: T - the value to find

        Returns
        -------
        Optional[_AVLTreeNode] - the node containing the value
            None if the value is not present
        """
        if self._root is None:
            return None
        return self._root.find(item, self._key(item))

    def __iter__(self) -> Generator[T, None, None]:
        """
        Iterate over the tree, in order from least to greatest

        Returns
        -------
        Generator[T, None, None] - lazily generates the values from least to greatest
        """
        if self._root is None:
            return
        for descendant in self._root:
            yield descendant.value

    def add(self, item: T) -> bool:
        """
        Add a value to the tree, if not already present

        Parameters
        ----------
        item: T - the value to try to add

        Returns
        -------
        bool - if the addition was successful or not
            True if the value was added
            False if the value was already present
        """
        if self._root is None:
            self._root = _AVLTreeNode(item, key=self._key)
            success = True
        else:
            success = self._root.add(item, self._key(item))
        if success:
            self._count += 1
        return success

    def remove(self, item: T) -> bool:
        """
        Remove a value from the tree, if present

        Parameters
        ----------
        item: T - the value to try to remove

        Returns
        -------
        bool - if the removal was successful or not
            True if the value was found and remove
            False if the value was not present
        """
        if self._root is None:
            # nothing to remove
            return False
        # we need to check if we're removing the root
        item_key = self._key(item)
        root_key = self._key(self._root.value)
        # removing the root is special
        if item_key == root_key:

            if self._root.left is None:
                # re-point the root to the right child of the old root
                self._root = self._root.right
                # re-point the right child (the new root) to its new parent (None)
                if self._root is not None:
                    self._root.parent = None
            # self.left is not None
            elif self._root.right is None:
                # re-point the root to the left child of the old root
                self._root = self._root.left
                # re-point the left child (the new root) to its new parent (None)
                if self._root is not None:
                    self._root.parent = None
            # neither self.left nor self.right is None
            else:
                # go find the "in-order predecessor
                current = self._root.left
                while current.right is not None:
                    current = current.right
                # put its value into the current one
                self._root.value = current.value
                # remove the lower one
                current.remove(current.value, self._key(current.value))
                # even thought that call to current.remove is recursive,
                # we know it's already at the node it needs to remove,
                # and that that node has no right child,
                # so it will not recurse again
            success = True
        else:  # not any special situation
            success = self._root.remove(item, item_key)
        if success:
            self._count -= 1
        return success

    # TODO: bulk operations?
    # pylint: disable=line-too-long
    # https://en.wikipedia.org/wiki/AVL_tree#:~:text=log%20n)%20time.-,Set%20operations%20and%20bulk%20operations,-%5Bedit%5D

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
