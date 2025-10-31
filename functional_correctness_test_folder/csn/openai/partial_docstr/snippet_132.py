
import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        self.out = out

    def writerow(self, row):
        '''Write a single row.'''
        self.out.write(json.dumps(row))
        self.out.write('\n')
