#!/usr/bin/env python3
"""
Set of utilities that can be used with ShiftingBloomFilter:
    - CSVDataSet => a reader for data sets stored as CSV files
    - RandomStringGenerator => object used for generating random strings
    - HashFactory => object used for producing a list of salted hash functions
    - HashFunction => a salted hash function.
"""
#"It takes courage to choose hope over fear."
#   ~Mark Zuckerberg


from random import randint
from hashlib import algorithms_guaranteed
import hashlib
import pickle
from .exceptions import ERROR_MSGS, HashesUnavailableError

class HashFunction:
    """
        Wrapper around a salted hashing function.
    """

    def __init__(self, hash_base, salt):
        """
            HashFunction(
                hash_base => hash function to use for base,
                salt => salt to use for hashing.
            )
        """
        self.hash_base = hash_base
        self.salt = salt.encode()

    def __repr__(self):
        """return string representation of a salted hash function"""
        return "HashFunction(%s,%s)" % (repr(self.hash_base), str(self.salt))

    def __call__(self, data):
        """Return hash for data"""
        return self.hash_base(data + self.salt)


class HashFactory:
    """
        Object for creating salted hash functions.
        Produces a list of hash functions that can be used
        with ShiftingBloomFilter.
    """

    def __init__(self, hash_family, hash_count):
        """
            HashFactory(
                hash_family => a base for hash functions from hashlib
                hash_count  => number of hash functions to generate
            )

            Public methods:
            - save2file(filename) => save to file
            - (static) load_from_file(filename) => load from file

            ** supports: **
            - slicing
            - built-in len function
            - iterating over.
        """

        if hash_family not in algorithms_guaranteed:
            raise HashesUnavailableError(ERROR_MSGS.HASH_FUNCTION_UNAVAILABLE)
        self.hash_family = hash_family
        self.hash_base = getattr(hashlib, hash_family)
        self.hash_count = hash_count
        self.salts = []
        self.hash_funcs = []
        self.index = -1

        self.doubles = 0
        self._gen_hashes(hash_count)
        while self.doubles > 0:
            doubles, self.doubles = self.doubles, 0
            self._gen_hashes(doubles)

    def __repr__(self):
        """returns an representation of HashFactory object"""
        return "HashFactory(%s, %s)" % (
            str(self.hash_family),
            str(self.hash_count)
        )

    def save2file(self, filename="hash_data.bin"):
        """
            saves a list of hash functions to a binary file
            (void) save2file(
                filename => name of the file that hashes are to be saved to
            )
        """
        filehandle = None
        try:
            filehandle = open(filename, "wb")
            pickle.dump(self, filehandle)
        finally:
            if filehandle:
                filehandle.close()

    @staticmethod
    def load_from_file(filename="hash_data.bin"):
        """
            loads a list of hash functions from binary file
            (static) (void) load_from_file(
                filename => name of the file to read from
            )
        """
        datafile = None
        try:
            datafile = open(filename, "rb")
            hash_src = pickle.load(datafile)
        finally:
            if datafile:
                datafile.close()
        return hash_src

    def _gen_hashes(self, hash_count):
        """
            _gen_hashes(
                hash_count => amount of hash functions to generate
            )
            generate hash functions with random salts that are all different
        """

        for salt in RandomStringGenerator(stream_length=hash_count):
            if salt in self.salts:
                self.doubles += 1
                continue
            self.salts.append(salt)
            #h_func = lambda data, salt=salt: self.hash_base(data+salt.encode())
            self.hash_funcs.append(HashFunction(self.hash_base, salt))

    def __len__(self):
        """
            Length of the list with hash functions
        """
        return len(self.hash_funcs)

    def __iter__(self):
        """
            Iterator for hash function list
        """
        return self

    def __getitem__(self, val):
        """
            Slicing support for the function list
        """
        return self.hash_funcs[val]

    def __next__(self):
        """
            Next function in the iterator.
        """

        self.index += 1
        if self.index < self.hash_count:
            return self.hash_funcs[self.index]
        self.index = -1
        raise StopIteration


class CSVDataSet:
    """
        Iterative reader for csv data sets.
    """

    def __init__(self, filename, separator=','):
        """
           CSVDataSet(
                filename => name of the csv file
                separator => character used to separated values in csv file
                                                            (comma by default)
           )
        """
        self.filename = filename
        self.separator = separator
        self.file = open(filename)

    def __next__(self):
        """
            (tuple of values from csv file)
            Iterator, for iterating over values in CSV file,
            resets the file to position 0, after values have been exhaused.
        """

        csvs = self.file.readline().strip().split(self.separator)
        if len(csvs) > 1:
            return csvs
        self.file.seek(0)
        raise StopIteration

    def __repr__(self):
        """returns a representation of CSVDataSet"""
        return "CSVDataSet(%s, %s)" % (self.filename, self.separator)

    def __iter__(self):
        """
            Returns iterator for dataset.
        """
        return self


class RandomStringGenerator:
    """
        RandomStringGenerator, a stream of random strings of given length.
    """
    RANDOM_MIN = 4
    RANDOM_MAX = 32
    def __init__(self, string_length=4, ascii_start=32,
                 ascii_end=126, stream_length=...):
        """
            RandomStringGenerator(
                string_length => generate strings of this length
                ascii_start => start from this ascii character
                                            (takes in decimal representation)
                ascii_end => end at this ascii character
                                            (takes in decimal representation)
                stream_length => length of the stream, or '...' (elipsis) for
                                 infinite stream.
                )
        """

        self.length = string_length
        self.start = ascii_start
        self.end = ascii_end
        self.len = stream_length
        self.count = 0

    def __repr__(self):
        """Returns string representation of RandomStringGenerator"""
        return "RandomStringGenerator(%s, %s, %s, %s)" % (
            self.length,
            self.start,
            self.end,
            self.len
        )

    def __len__(self):
        """
            returns length of the stream or
            stream length so far for infinite streams
        """
        return self.len if self.len is not ... else self.count

    def __next__(self):
        """
            returns next string in the stream.
        """

        self.count += 1
        if self.len is not ... and self.count > self.len:
            raise StopIteration
        rand_s = ""
        if self.length is ...:
            rng = range(randint(RandomStringGenerator.RANDOM_MIN,
                                RandomStringGenerator.RANDOM_MAX))
        else:
            rng = range(self.length)
        for _ in rng:
            rand_s += chr(randint(self.start, self.end))
        return rand_s

    def __iter__(self):
        """
            returns the iterator for RandomStringGenerator
        """
        return self
