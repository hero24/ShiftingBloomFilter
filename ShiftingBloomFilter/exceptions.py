#!/usr/bin/env python3
"""
Module containing ShiftingBloomFilter specific exceptions
"""
class ERROR_MSGS:
    """
        Container for possible error messages.
    """

    NOT_ENNOUGH_HASHES = ("The value given for hash_count exceeds "
                          "amount of available hash functions.")
    HASH_FUNCTION_UNAVAILABLE = "Given hash funtion is unavailable."


class HashesUnavailableError(ValueError):
    """
        Exception raised when there is error related to hashing functions
    """
    def __init__(self, message, *args, **kwargs):
        super().__init__(args, kwargs)
        self.message = message

    def __str__(self):
        return self.message
