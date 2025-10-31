
import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        '''Initialize with output destination.'''
        self.out = out

    def writerow(self, row):
        '''Write a single row.'''
        self.out.write(json.dumps(row) + '\n')
