from collections.abc import Iterable as IterableABC, Mapping as MappingABC
from itertools import chain
from typing import Any, Generator, Generic, Iterable, List, Mapping, Optional, Tuple, TypeVar, Union


K = TypeVar("K")
V = TypeVar("V")


class _TreeMapNode(Generic[K, V]):
    """
    Intended only as a "helper class" to TreeMap.
    Stores a single key/value pair, as well as connections that define the tree structure.
    """
    __slots__ = "key", "value", "left", "right", "parent"

    def __init__(self,
                 key: K,
                 value: V,
                 *,
                 left: "_TreeMapNode[K, V]" = None,
                 right: "_TreeMapNode[K, V]" = None,
                 parent: "_TreeMapNode[K, V]" = None):
        """
        Construct a node of a binary tree.
        TODO: make it self-balancing

        Parameters
        ----------
        key: K - the key used for sorting and comparing this node against others
        value: T - the value to be stored in this node
        left: _TreeMapNode[K, V] - the left child of this node, by default None
        right: _TreeMapNode[K, V] - the right child of this node, by default None
        parent: _TreeMapNode[K, V] - the parent of this node, by default None
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def __iter__(self) -> Generator["_TreeMapNode[K, V]", None, None]:
        raise NotImplementedError

    def get(self, key: K) -> Optional["_TreeMapNode[K, V]"]:
        raise NotImplementedError

    def get_set_default(self, key: K, default: V = None) -> Optional["_TreeMapNode[K, V]"]:
        raise NotImplementedError

    def remove(self, key: K) -> V:
        # TODO: if key not present, raise KeyError(key)
        raise NotImplementedError

    def set(self, key: K, value: V) -> bool:
        raise NotImplementedError


class TreeMap(MappingABC, Generic[K, V]):
    """
    A dictionary/map object, backed by a binary tree.
    Naturally keeps items sorted by keys.

    `K` represents the type of keys.
    `V` represents the type of values.

    Keys are ordered using `<` and `>`, and key (in)equality is checked using `==` and `!=`.
    """
    __slots__ = "_root", "_count"

    def __init__(self):
        """
        Construct a TreeMap.
        """
        self._root: Optional[_TreeMapNode[K, V]] = None
        self._count = 0

    def clear(self):
        """
        Empty all data from the TreeMap.

        Returns
        -------
        None
        """
        self._root = None
        self._count = 0

    def get(self, key: K, default: V = None) -> V:
        """
        Return the value for key if key is in the map, else default.
        If default is not given, it defaults to None, so that this method never raises a KeyError

        Parameters
        ----------
        key: K - The key to search for and retrieve a value for.
        default: V - The value to return if the key is not present.
            None, by default.

        Returns
        -------
        V - The value associated with the given key, or `default` if the key is not present.
        """
        # go looking
        result_node: Optional[_TreeMapNode[K, V]] = \
            None if self._root is None else self._root.get(key)
        # did we find it?
        if result_node is None:
            if default is None:
                raise KeyError(key)
            # else:
            return default
        # else:
        return result_node.value

    def items(self) -> List[Tuple[K, V]]:
        """
        Return a new view of the map’s items ((key, value) pairs),
        sorted by keys.

        Returns
        -------
        List[Tuple[K, V]] - A list of tuples, each being a (key, value) pair.
            sorted by keys.
        """
        if self._root is None:
            return []
        return [(node.key, node.value) for node in self._root]

    def keys(self) -> List[K]:
        """
        Return a new view of the map's keys, sorted.

        Returns
        -------
        List[K] - A list of keys, sorted.
        """
        if self._root is None:
            return []
        return [node.key for node in self._root]

    def values(self) -> List[V]:
        """
        Return a new view of the map’s values, sorted by their keys (which are not given here).

        Returns
        -------
        List[V] - A list of values, sorted by keys (which are not given here).
        """
        if self._root is None:
            return []
        return [node.value for node in self._root]

    def pop(self, key: K, default: V = None) -> V:
        """
        If key is in the map, remove it and return its value, else return default.
        If default is None and key is not in the map, a KeyError is raised.

        Parameters
        ----------
        key: K - The key to search for and remove.
        default: V - The value to return if the key is not present.
            None, by default.

        Raises
        ------
        KeyError - If the key is not in the map and default is None.

        Returns
        -------
        V - The value associated with the given key, or `default` if the key is not present.
        """
        try:
            if self._root is None:  # nothing to remove
                raise KeyError(key)
            # we need to check if we're removing the root;
            # removing the root is special
            if key == self._root.key:
                removed_value = self._root.value
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
                    # go find the "in-order predecessor"
                    current = self._root.left
                    while current.right is not None:
                        current = current.right
                    # put its value into the current one
                    self._root.value = current.value
                    # remove the lower one
                    current.remove(current.key)
                    # even thought that call to current.remove is recursive,
                    # we know it's already at the node it needs to remove,
                    # and that that node has no right child,
                    # so it will not recurse again
            else:  # not any special situation
                removed_value = self._root.remove(key)
        except KeyError:  # couldn't find it
            if default is None:
                raise KeyError(key)
            # else:
            return default
        else:  # we did find it
            self._count -= 1
            return removed_value

    def popitem(self) -> Tuple[K, V]:
        """
        Remove and return a (key, value) pair from the map.
        The pair removed is always the root node of the backing binary tree.
        popitem() is useful to destructively iterate over a map, as often used in set algorithms.
        If the map is empty, calling popitem() raises a KeyError.

        Raises
        ------
        KeyError - If the map is empty.

        Returns
        -------
        Tuple[K, V] - A (key, value) pair that was removed from the map.
            Before removal, this pair was the root node of the tree.
        """
        if self._root is None:
            raise KeyError("map is empty")
        # what key to pop?
        key = self._root.key
        # pop it
        try:
            removed_value = self.pop(key)
        except KeyError as e:
            raise RuntimeError("programmer error") from e
        return key, removed_value

    def setdefault(self, key: K, default: V = None) -> V:
        """
        If key is in the map, return its value.
        If not, insert key with a value of default and return default.

        Parameters
        ----------
        key: K - The key to search for and retrieve a value for.
        default: V - The value to insert and return if the key is not initially present.
            None, by default.

        Returns
        -------
        V - The value associated with the given key,
            or `default` if the key is not initially present.
        """
        if self._root is None:
            self._root = _TreeMapNode(key, default)
            self._count += 1
            return default
        result_node = self._root.get_set_default(key, default)
        if result_node is None:  # used the default
            self._count += 1
            return default
        # else: just getting a value, not setting
        return result_node.value

    def update(self, other: Union[Mapping[K, V], Iterable[Tuple[K, V]]], **kwargs):
        """
        Update the map with the key/value pairs from `other`, overwriting existing keys.
        update() accepts either another Mapping object or an Iterable of key/value pairs
        (as tuples or other iterables of length two). If keyword arguments are specified,
        the map is then updated with those key/value pairs: `m.update(red=1, blue=2)`
        Iterates over `other`, repeatedly calling __setitem__

        Parameters
        ----------
        other: Union[Mapping[K, V], Iterable[Tuple[K, V]]] -
            A Mapping object or Iterable object to provide new key/value pairs
        kwargs - Keyword arguments, e.g. `red=1`, in which case the key/value pair
            `("red", 1)` would be written to the map.

        Returns
        -------
        None
        """
        if isinstance(other, MappingABC):
            tup_iter = other.items()
        elif isinstance(other, IterableABC):
            tup_iter = other
        else:
            raise TypeError(f"`new_pairs` must be a Mapping or Iterable "
                            f"(actual class is {other.__class__})")
        for key, value in chain(tup_iter, kwargs.items()):
            self.__setitem__(key, value)

    def __contains__(self, key: K) -> bool:
        """
        Check if a key is present in the map.

        Parameters
        ----------
        key: K - The key to search for.

        Returns
        -------
        bool - True if the key is in the map, False if not.
        """
        if self._root is None:
            return False
        return key in self._root

    def __delitem__(self, key: K):
        """
        Remove the key and its value from the map.
        Raises a KeyError if the key is not in the map.

        Parameters
        ----------
        key: K - The key to search for and remove.

        Raises
        ------
        KeyError - If the key is not in the map.

        Returns
        -------
        None
        """
        try:
            if self._root is None:
                raise KeyError(key)
            result = self._root.remove(key)
        except KeyError:
            raise KeyError(key)
        else:
            self._count -= 1
            return result

    def __eq__(self, other: Any) -> bool:
        """
        Check if the map is equal to another object.
        The other object will not be considered equal if it is of any other class.
        Both keys and values are compared using the `!=` operator.

        Parameters
        ----------
        other: Any - The object to compare to.

        Returns
        -------
        bool - True if `other` is also a TreeMap and has the same key/value pairs,
            False otherwise.
        """
        if not isinstance(other, self.__class__):
            # not the same class even
            return False
        if self._root is None and other._root is None:
            # both empty
            return True
        if len(self) != len(other):
            return False
        for self_node, other_node in zip(self._root, other._root):
            if self_node.key != other_node.key:
                return False
            if self_node.value != other_node.value:
                return False
        return True

    def __getitem__(self, key: K) -> V:
        """
        Return the value associate with the given key.
        Raises a KeyError if key is not in the map.

        Parameters
        ----------
        key: K - The key to search for and retrieve a value for.

        Raises
        ------
        KeyError - If the key is not in the map.

        Returns
        -------
        V - The value associated with the given key.
        """
        if self._root is None:
            result_node = None
        else:
            result_node = self._root.get(key)
        if result_node is None:
            raise KeyError(key)
        return result_node.value

    def __setitem__(self, key: K, value: V):
        """
        Set the given key's value to the given value.
        Can be used to overwrite the value of an existing key, or to insert a new key/value pair.

        Parameters
        ----------
        key: K - The key where the value should be written.
        value: V - The value to be written.

        Returns
        -------
        None
        """
        if self._root is None:
            self._root = _TreeMapNode(key, value)
            is_new = True
        else:
            is_new = self._root.set(key, value)
        if is_new:
            self._count += 1

    def __iter__(self) -> Generator[K, None, None]:
        """
        Iterate over the map, in order from least to greatest (by keys).

        Returns
        -------
        Generator[K, None, None] - lazily generates the keys from least to greatest
        """
        if self._root is None:
            return  # just terminate
        for node in self._root:
            yield node.key

    def __len__(self) -> int:
        """
        Return the number of items in the map.

        Returns
        -------
        int - The number of key/value pairs in the map.
        """
        return self._count

    def __ne__(self, other: Any) -> bool:
        """
        Calls __eq__ and negates the result. See __eq__.

        Parameters
        ----------
        other: Any - The object to compare to.

        Returns
        -------
        bool - False if `other` is also a TreeMap and has the same key/value pairs,
            True otherwise.
        """
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """
        Give a simple string representation of the map.
        For debugging purposes.

        Returns
        -------
        str - A simple string value to represent the map.
        """
        return f"{self.__class__.__name__}(len={self.__len__()})"

    __hash__ = None
