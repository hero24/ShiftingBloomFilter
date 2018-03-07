#!/usr/bin/env python3
class ERROR_MSGS:
    NOT_ENNOUGH_HASHES = ("The value given for hash_count exceeds " 
                         "amount of available hash functions.")
    HASH_FUNCTION_UNAVAILABLE = "Given hash funtion is unavailable."
    DILL_NOT_FOUND = ("Cannot load dill module which is required"
                      " for saving data to file.")

class HashesUnavailableError(ValueError):
    def __init__(self,message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message

class SerializationError(ImportError):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
