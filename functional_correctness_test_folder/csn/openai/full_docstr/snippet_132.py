
import json


class JsonWriter:
    '''Utility for dumping rows as JSON objects.'''

    def __init__(self, out):
        '''Initialize with output destination.'''
        # `out` is expected to be a file‑like object with a write() method.
        self.out = out

    def writerow(self, row):
        '''Write a single row.'''
        # Convert the row to a JSON string and write it followed by a newline.
        self.out.write(json.dumps(row))
        self.out.write('\n')
