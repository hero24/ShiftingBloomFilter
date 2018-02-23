#!/usr/bin/env python3
import hashlib
from hashlib import algorithms_guaranteed
from sys import byteorder
from inspect import signature
from .Exceptions import HashesUnavailableError, ERROR_MSGS
class ShiftingBloomFilter:
    def __init__(self, length,hash_count=len(algorithms_guaranteed)):
        """
        ShiftingBlomFilter(
            length => the size of the underlying bytearray which is used to
                                                    represent the filter.
            hash_count => amount of hashing functions to use. 
                          NOTE: cannot be greater than length 
                                                    of algorithms_guaranteed
        )
        """
        if hash_count > len(algorithms_guaranteed):
            raise HashesUnavailableError(ERROR_MSGS.NOT_ENNOUGH_HASHES)
        self.m = length
        self.k = hash_count
        self.cut_off = int(self.k//2)
        self.hashfunc = [getattr(hashlib,h) for h in algorithms_guaranteed]
        self.hashfunc = self.hashfunc[0:self.k]
        self.filter = bytearray(self.m)
        self.max_set = 0

    def _get_hash(self,h,s,offset):
        """
        (int) returns a position in array calculated from a hash of an object.
            _get_hash(
                h => hash function
                s => object to be hashed
                offset => offset for hash value
            )
        """
        hashed_value = h(s.encode())
        try:
            # temporary work around => FIX later;
            if len(signature(hashed_value.digest).parameters) > 0:
                hashed_value = hashed_value.digest(100)
            else:
                hashed_value = hashed_value.digest()
        except ValueError:
            hashed_value = hashed_value.digest()
        return (int.from_bytes(hashed_value, byteorder) + offset ) % self.m

    def _set_position(self,h,item,set_no=0):
        """
            (void) sets position in byte array for given item using given 
                   hash function to indicate that item is in the set. For 
                   multiple sets, a set id might be specified.
            _set_position(
                h => hash function
                item => object to store
                set_no => this is the id of the set, by default 0
            )
        """
        self.filter[self._get_hash(h,item,set_no)] = 1

    def _check_position(self,h,item,set_no=0):
        """
            (boolean) checks if the position for the given item and hash 
                      function indicates that the item might be in the set.
            _check_position(
                h => hash function
                item => object to check for
                set_no => set id that object shoud belong to, by default 0
            )
        """
        return self.filter[self._get_hash(h,item,set_no)] == 1
       
    def insert(self,item,set_no=0):
        """
            (void) inserts item to bloom filter
            insert(
                item => item to insert
                set_no => which set is the item supposed to go in, by default 0
            )
        """
        if set_no > self.max_set:
            self.max_set = set_no
        for h in self.hashfunc[:self.cut_off]:
            self._set_position(h,item)
        for h in self.hashfunc[self.cut_off:]:
            self._set_position(h,item,set_no)

    def check(self,item):
        """
            (boolean, list of set ids that item might possibly be in) 
            checks the possibility of item being in a set
            check(
                item => item to check for
            )
        """
        for h in self.hashfunc[:self.cut_off]:
            if not self._check_position(h,item):
                return False,[]
        return self._check_offsets(item)

    def _check_offsets(self,item):
        """
            (boolean, list of set ids that item might possibly be in)
            checks the sets that item might be in.
            _check_offsets(
                item => item to check for.
            )
        """
        set_no =  0
        possible_sets = []
        while self.max_set >= set_no:
            found = True
            for h in self.hashfunc[self.cut_off:]:
                if not self._check_position(h,item,set_no):
                    found = False
                    break
            if found:
                possible_sets.append(set_no)
            set_no += 1 
        return (len(possible_sets) > 0,possible_sets)

