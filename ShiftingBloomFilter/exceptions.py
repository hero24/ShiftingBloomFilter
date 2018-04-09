#!/usr/bin/env python3
"""
Module containing ShiftingBloomFilter specific exceptions
    Exceptions:
    - SBFException => ShifingBloomFilter base top-level module exception.
    - HashesUnavailableError => Exception raised when there is problem with
                                hash function avaialbilty.

    Other objects:
    - ERROR_MSGS => Wrapper around all the possible error messages.
"""

# "Some people dream of success,
#  while others wake up and work hard at it."
#           ~ Mark Zuckerberg

class ERROR_MSGS:
    """
        Container for possible error messages.
    """

    NOT_ENNOUGH_HASHES = ("The value given for hash_count exceeds "
                          "amount of available hash functions.")
    HASH_FUNCTION_UNAVAILABLE = "Given hash funtion is unavailable."


class SBFException(Exception):
    """
        Top-level module exception
    """
    pass

class HashesUnavailableError(SBFException, ValueError):
    """
        Exception raised when there is error related to hashing functions
    """
    def __init__(self, message, *args, **kwargs):
        super().__init__(args, kwargs)
        self.message = message

    def __str__(self):
        return self.message
