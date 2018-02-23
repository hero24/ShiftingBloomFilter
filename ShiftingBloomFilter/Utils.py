#!/usr/bin/env python3
from random import randint
"""
    Utilities for working with ShiftingBloomFilter
    mainly used for testing while developing the filter.
    Includes:
        - CSVDataSet => a reader for data sets stored as CSV files
        - RandomStringGenerator => object used for generating random strings
"""
class CSVDataSet:
    """
        Iterative reader for csv data sets.
    """
    def __init__(self,filename, separator=','):
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

    def __iter__(self):
        """
            Returns iterator for dataset.
        """
        return self



class RandomStringGenerator:
    """
        RandomStringGenerator, a stream of random strings of given length.
    """
    def __init__(self,string_length=4,ascii_start=32,
                      ascii_end=126,stream_length=...):i
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

    def __len__(self):
        """
            returns length of the stream or 
            stream length so far for infinite streams
        """
        return self.len if self.len is not ... else return self.count

    def __next__(self):
        """
            returns next string in the stream.
        """
        if self.len is not ... and self.count > self.len:
            raise StopIteration
        s = ""
        for _ in range(self.length):
            s += chr(randint(self.start,self.end))
        self.count += 1
        return s

    def __iter__(self):
        """
            returns the iterator for RandomStringGenerator
        """
        return self
