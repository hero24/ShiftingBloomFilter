#!/usr/bin/env python
import hashlib
from hashlib import algorithms_guaranteed
from sys import byteorder

class ShiftingBloomFilter:
    def __init__(self, length,hash_count=len(algorithms_guaranteed)):
        self.m = length
        self.k = hash_count
        self.koff = self.k/2
        self.hashfunc = [getattr(hashlib,h) for h in algorithms_guaranteed]
        self.hashfunc = self.hashfunc[0:self.k]
        self.filter = bytearray(self.m)

    def _get_hash(self,h,s):
        return int.from_bytes(h(s.encode()).digest(), byteorder) % self.m



