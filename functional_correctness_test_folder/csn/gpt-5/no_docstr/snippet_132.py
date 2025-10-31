import json


class JsonWriter:

    def __init__(self, out):
        if not hasattr(out, "write"):
            raise TypeError("out must be a writable file-like object")
        self._out = out

    def writerow(self, row):
        self._out.write(json.dumps(row, ensure_ascii=False, default=str))
        self._out.write("\n")
