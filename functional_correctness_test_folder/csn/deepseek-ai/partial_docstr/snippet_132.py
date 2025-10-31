
import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        self.out = out

    def writerow(self, row):
        '''Write a single row.'''
        json.dump(row, self.out)
        self.out.write('\n')
