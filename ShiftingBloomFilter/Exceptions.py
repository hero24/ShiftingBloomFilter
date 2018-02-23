#!/usr/bin/env python3
class ERROR_MSGS:
    NOT_ENNOUGH_HASHES = ("The value given for hash_count exceeds " 
                         "amount of available hash functions")

class HashesUnavailableError(ValueError):
    def __init__(self,message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
