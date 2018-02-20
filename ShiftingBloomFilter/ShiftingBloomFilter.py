#!/usr/bin/env python3
import hashlib
from hashlib import algorithms_guaranteed
from sys import byteorder

class ShiftingBloomFilter:
    def __init__(self, length,hash_count=len(algorithms_guaranteed)):
        self.m = length
        self.k = hash_count
        self.cut_off = int(self.k/2)
        self.hashfunc = [getattr(hashlib,h) for h in algorithms_guaranteed]
        self.hashfunc = self.hashfunc[0:self.k]
        self.filter = bytearray(self.m)
        self.max_set = 0

    def _get_hash(self,h,s,offset=0):
        return (int.from_bytes(h(s.encode()).digest(), byteorder)+ offset) % self.m

    def _set_position(self,h,item,set_no=0):
        self.filter[self._get_hash(h,item,set_no)] = 1

    def _check_position(self,h,item,set_no=0):
        return self.filter[self._get_hash(h,item,set_no)] == 1

    def insert(self,item,set_no=0):
        if set_no > self.max_set:
            self.max_set = set_no
        for h in self.hashfunc[:self.cut_off]:
            self._set_position(h,item)
        for h in self.hashfunc[self.cut_off:]:
            self._set_position(h,item,set_no)

    def check(self,item):
        for h in self.hashfunc[:self.cut_off]:
            if not self._check_position(h,item):
                return False,[]
        return self._check_offsets(item)

    def _check_offsets(self,item):
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

