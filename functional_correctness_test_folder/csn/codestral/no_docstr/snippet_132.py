
import json


class JsonWriter:

    def __init__(self, out):
        self.out = out
        self.first_row = True

    def writerow(self, row):
        if self.first_row:
            self.out.write('[')
            self.first_row = False
        else:
            self.out.write(',')
        json.dump(row, self.out)
