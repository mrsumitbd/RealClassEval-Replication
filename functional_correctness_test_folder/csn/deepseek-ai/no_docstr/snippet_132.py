
import json


class JsonWriter:

    def __init__(self, out):
        self.out = out
        self.first_row = True
        self.out.write('[')

    def writerow(self, row):
        if not self.first_row:
            self.out.write(',')
        json.dump(row, self.out)
        self.first_row = False

    def close(self):
        self.out.write(']')
        self.out.close()
