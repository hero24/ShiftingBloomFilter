#!/usr/bin/env python3

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


