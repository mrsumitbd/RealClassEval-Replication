import csv

class UnicodeReader:

    def __init__(self, f, encoding=None, errors='strict', **csvargs):
        f = UTF8Recoder(f, encoding=encoding, errors=errors)
        self.reader = csv.reader(f, **csvargs)

    def next(self):
        row = self.reader.next()
        return [unicode(s, 'utf-8') if isinstance(s, basestring) else s for s in row]

    def __iter__(self):
        return self