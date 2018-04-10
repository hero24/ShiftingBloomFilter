#!/usr/bin/env python3
"""Module containing an implementation of  Shifting Bloom Filter.

Bloom filter is a space efficient probabilistic data structure used for testing
if an element is in a set. Shifting Bloom filter is an extension on the standard
Bloom filter, that supports multiple sets or multisets.

Available objects:
- ShiftingBloomFilter => Shifting Bloom Filter

Available constants:
- MULTISET - mode of operation of ShiftingBloomFilter where the filter is used
           with multiset (a set that can have more than one of thesame element)
- MULTIPLE - mode of operation of ShiftingBloomFilter where the filter is used
           with many different sets.

Available submodules:
- utils => utilities that can be used with ShiftingBloomFilter
- visualiser => GUI tool for visualising the filter.
- exceptions => all possible exceptions that can be thrown by objects in
                this module
"""

from ShiftingBloomFilter.shifting_bloom_filter import ShiftingBloomFilter
from ShiftingBloomFilter.shifting_bloom_filter import MULTISET, MULTIPLE
import ShiftingBloomFilter.utils as utils
import ShiftingBloomFilter.exceptions as exceptions
__all__ = ["ShiftingBloomFilter", "utils", "exceptions", "MULTISET", "MULTIPLE"]
