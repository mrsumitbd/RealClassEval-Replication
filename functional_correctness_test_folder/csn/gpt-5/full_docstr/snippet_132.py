import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        '''Initialize with output destination.'''
        if not hasattr(out, 'write'):
            raise TypeError(
                'out must be a file-like object with a write() method')
        self._out = out

    def writerow(self, row):
        '''Write a single row.'''
        s = json.dumps(row, ensure_ascii=False,
                       separators=(',', ':'), default=str)
        self._out.write(s + '\n')
