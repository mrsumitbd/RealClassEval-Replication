
import json


class JsonWriter:

    def __init__(self, out):
        self.out = out
        self.first_row = True
        self.out.write('[')

    def writerow(self, row):
        if not self.first_row:
            self.out.write(', ')
        else:
            self.first_row = False
        self.out.write(json.dumps(row))

    def __del__(self):
        try:
            self.out.write(']')
        except Exception:
            pass
