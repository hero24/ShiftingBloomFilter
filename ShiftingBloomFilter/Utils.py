#!/usr/bin/env python3
from random import randint

class CSVDataSet:
    def __init__(self,filename, separator=','):
        self.filename = filename
        self.separator = separator
        self.file = open(filename)
       
       
    def __next__(self):
        csvs = self.file.readline().strip().split(self.separator)
        if len(csvs) > 1:
            return csvs
        self.file.seek(0)
        raise StopIteration

    def __iter__(self):
        return self



class RandomStringGenerator:
    def __init__(self,string_length=4,ascii_start=32,ascii_end=126,stream_length=...):
        self.length = string_length
        self.start = ascii_start
        self.end = ascii_end
        self.len = stream_length
        self.count = 0

    def __len__(self):
        return self.len

    def __next__(self):
        if self.len is not ... and self.count > self.len:
            raise StopIteration
        s = ""
        for _ in range(self.length):
            s += chr(randint(self.start,self.end))
        self.count += 1
        return s

    def __iter__(self):
        return self
