
import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        self.out = out
        self.first_row = True

    def writerow(self, row):
        '''Write a single row.'''
        if not self.first_row:
            self.out.write(',\n')
        self.out.write(json.dumps(row))
        self.first_row = False
