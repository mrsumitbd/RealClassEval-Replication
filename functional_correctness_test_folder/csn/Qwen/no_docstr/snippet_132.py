
import json


class JsonWriter:

    def __init__(self, out):
        self.out = out
        self.data = []

    def writerow(self, row):
        self.data.append(row)

    def writeall(self):
        json.dump(self.data, self.out, indent=4)
        self.out.write('\n')
