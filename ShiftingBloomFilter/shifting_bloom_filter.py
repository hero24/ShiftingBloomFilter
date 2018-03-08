#!/usr/bin/env python3i

"""
 Python implementation of shifting bloom filter.
"""

import hashlib
from hashlib import algorithms_guaranteed
import pickle as pickle
from sys import byteorder
from inspect import signature
from .exceptions import HashesUnavailableError, ERROR_MSGS


class ShiftingBloomFilter:
    """
        ShiftingBloomFilter => bloom filter with support for handling multiple
                               sets. Implements shifting bloom filter.
    """

    def __init__(self, length, hash_count=len(algorithms_guaranteed),
                 hash_source=algorithms_guaranteed, length_as_power=True):
        """
        ShiftingBlomFilter(
            length => the size of the underlying bytearray which is used to
                                                    represent the filter.
            hash_count => amount of hashing functions to use.
                          NOTE: cannot be greater than length
                                                    of hash source
            hash_source => a list of hashing functions to use
            length_as_power => is the length of the filter expressed
                                as power of 2 (True) or is it literal (False)
        )
        """

        if hash_count > len(hash_source):
            raise HashesUnavailableError(ERROR_MSGS.NOT_ENNOUGH_HASHES)
        self.m = 2**length if length_as_power else length
        self.k = hash_count
        self.cut_off = self.k//2
        self.hashfunc = ([getattr(hashlib, name) for name in algorithms_guaranteed]
                       if hash_source is algorithms_guaranteed else hash_source)
        self.hashfunc = self.hashfunc[:self.k]
        self.filter = bytearray(self.m)
        self.max_set = 0

    def __len__(self):
        """
            (int) returns the length of the underlying bytearray
        """
        return self.m

    def __getitem__(self, index):
        """
            (int) [index] => returns index position of the underlying bytearray
        """
        return self.filter[index]

    def _get_hash(self, hash_fn, data, offset):
        """
        (int) returns a position in array calculated from a hash of an object.
            _get_hash(
                hash_fn => hash function to use for hashing
                data => object to be hashed
                offset => offset for hash value
            )
        """

        hashed_value = hash_fn(data.encode())
        try:
            # temporary work around => FIX later;
            if signature(hashed_value.digest).parameters:
                hashed_value = hashed_value.digest(100)
            else:
                hashed_value = hashed_value.digest()
        except ValueError:
            hashed_value = hashed_value.digest()
        return (int.from_bytes(hashed_value, byteorder) + offset) % self.m

    def _set_position(self, hash_fn, item, set_no=0):
        """
            (void) sets position in byte array for given item using given
                   hash function to indicate that item is in the set. For
                   multiple sets, a set id might be specified.
            _set_position(
                hash_fn => hash function
                item => object to store
                set_no => this is the id of the set, by default 0
            )
        """
        self.filter[self._get_hash(hash_fn, item, set_no)] = 1

    def _check_position(self, hash_fn, item, set_no=0):
        """
            (boolean) checks if the position for the given item and hash
                      function indicates that the item might be in the set.
            _check_position(
                hash_fn => hash function
                item => object to check for
                set_no => set id that object shoud belong to, by default 0
            )
        """
        return self.filter[self._get_hash(hash_fn, item, set_no)] == 1

    def insert(self, item, set_no=0):
        """
            (void) inserts item to bloom filter
            insert(
                item => item to insert
                set_no => which set is the item supposed to go in, by default 0
            )
        """

        if set_no > self.max_set:
            self.max_set = set_no
        for hash_fn in self.hashfunc[:self.cut_off]:
            self._set_position(hash_fn, item)
        for hash_fn in self.hashfunc[self.cut_off:]:
            self._set_position(hash_fn, item, set_no)

    def check(self, item):
        """
            (boolean, list of set ids that item might possibly be in)
            checks the possibility of item being in a set
            check(
                item => item to check for
            )
        """

        for hash_fn in self.hashfunc[:self.cut_off]:
            if not self._check_position(hash_fn, item):
                return False, []
        return self._check_offsets(item)

    def _check_offsets(self, item):
        """
            (boolean, list of set ids that item might possibly be in)
            checks the sets that item might be in.
            _check_offsets(
                item => item to check for.
            )
        """

        set_no = 0
        possible_sets = []
        while self.max_set >= set_no:
            for hash_fn in self.hashfunc[self.cut_off:]:
                if not self._check_position(hash_fn, item, set_no):
                    break
            else:
                possible_sets.append(set_no)
            set_no += 1
        return (len(possible_sets) > 0, possible_sets)

    def save2file(self, filename="sbf.bin"):
        """
            (void) save filter to a binary file
        """
        with open(filename, "wb") as datafile:
            pickle.dump(self, datafile)

    @staticmethod
    def load_from_file(filename="sbf.bin"):
        """
            (static) (ShiftingBloomFilter)
            restore a filter from binary file.
        """
        with open(filename, "rb") as sbf:
            return pickle.load(sbf)