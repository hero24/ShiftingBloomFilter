#!/usr/bin/env python3
""" Python implementation of shifting bloom filter."""

#"It seems like the right thing to do is tackle problems
# other people aren't working on" ~Sean Parker

import hashlib
from hashlib import algorithms_guaranteed
import pickle as pickle
from sys import byteorder
import math
from .exceptions import HashesUnavailableError, ERROR_MSGS

MULTIPLE = True
MULTISET = not MULTIPLE


class ShiftingBloomFilter:
    """
        ShiftingBloomFilter => bloom filter with support for handling multiple
                               sets or multisets
    """

    def __init__(self, length, hash_source=algorithms_guaranteed,
                 hash_count=None, length_as_power=True, mode=MULTIPLE,
                 set_count=0):
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
            mode => MULTIPLE if there are multiple sets or MULTISET if its one
                    set but supporting multiple elements.
            set_count => how many sets is this filter supposed to support?
        )

        ** NOTE: every hashing function must have a digest function that takes
                 no arguments. If 'shake' functions are provided by
                 algorithms_guaranteed (the default) they are dropped because,
                 they require a parameter in the digest function
        **

        public methods:
        - insert(item, set_no) => insert item into filter with set_no
        - check(item) => check if item is in the filter
        - save2file(filename) => save filter to file
        - (static) load_from_file(filename) => load filter from file
        """
        self.m = 2**length if length_as_power else length
        self.hashfunc = (
            [getattr(hashlib, name) for name in algorithms_guaranteed
             if "shake" not in name.lower()]
            if hash_source is algorithms_guaranteed else hash_source
        )
        if hash_count is None:
            hash_count = len(self.hashfunc)
        if hash_count > len(hash_source):
            raise HashesUnavailableError(ERROR_MSGS.NOT_ENNOUGH_HASHES)
        self.k = hash_count
        self.cut_off = self.k//2
        self.hashfunc = self.hashfunc[:self.k]
        self.filter = bytearray(self.m)
        self.max_set = set_count
        self.length_as_power = length_as_power
        self.hash_source = hash_source
        self.mode = mode
        self.count = 0

    def __len__(self):
        """(int) returns the length of the underlying bytearray"""
        return self.m

    def __bool__(self):
        """(boolean) returns if the filter is not empty"""
        for i in self.filter:
            if i:
                return True
        return False

    def __str__(self):
        """return string representation of the filter"""
        str_ = ""
        for i in self.filter:
            str_ += " " + str(i)
        str_ += " "
        return str_

    def __repr__(self):
        """return string representation of an object constructor"""
        return "ShiftingBloomFilter(%s, %s, %s, %s, %s, %s)" % (
            self.m if not self.length_as_power else int(math.log2(self.m)),
            self.hash_source,
            self.k,
            self.length_as_power,
            self.mode,
            self.max_set
        )

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

        hashed_value = hash_fn(data.encode()).digest()
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
                          if working with multiple sets.
            )
        """
        if self.mode:
            self._insert_at_offset(item, set_no)
        else:
            in_set, count = self.check(item)
            if in_set:
                self._insert_at_offset(item, count+1)
            else:
                self._insert_at_offset(item, 0)
        self.count += 1

    def _insert_at_offset(self, item, offset):
        """
            (void) inserts item with 'offset' as an offset
            _insert_at_offset(
                item => item to insert
                offset => offset to use while hashing
            )
        """
        if offset > self.max_set:
            self.max_set = offset
        for hash_fn in self.hashfunc[:self.cut_off]:
            self._set_position(hash_fn, item)
        for hash_fn in self.hashfunc[self.cut_off:]:
            self._set_position(hash_fn, item, offset)

    def check(self, item):
        """
            (boolean, list of set ids that item might possibly be in) or
            (boolean, possible count of items in the set)
            checks the possibility of item being in a set
            check(
                item => item to check for
            )
        """

        for hash_fn in self.hashfunc[:self.cut_off]:
            if not self._check_position(hash_fn, item):
                if self.mode:
                    return False, []
                return False, 0
        return self._check_offsets(item)

    def _check_offsets(self, item):
        """
            (boolean, list of set ids that item might possibly be in) or
            (boolean, possible count of items in the set)
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
        if self.mode:
            return (len(possible_sets) > 0, possible_sets)
        return (len(possible_sets) > 0, len(possible_sets))

    def save2file(self, filename="sbf.bin"):
        """(void) save filter to a binary file"""

        with open(filename, "wb") as datafile:
            pickle.dump(self, datafile)

    def get_fpr(self):
        """
            (Number) returns false positve rate for current state
            of the filter
        """
        p = math.e ** ((-self.count * self.k)/len(self))
        fpr = ((1-p)**(self.k/2)) * (1 - p + (1/(self.max_set+1)) * (p**2))
        return fpr

    @staticmethod
    def load_from_file(filename="sbf.bin"):
        """
            (static) (ShiftingBloomFilter)
            restore a filter from binary file.
        """
        with open(filename, "rb") as sbf:
            return pickle.load(sbf)
