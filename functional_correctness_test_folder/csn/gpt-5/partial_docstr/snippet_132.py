import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        self._out = out

    def writerow(self, row):
        '''Write a single row.'''
        self._out.write(json.dumps(row, ensure_ascii=False))
        self._out.write('\n')
