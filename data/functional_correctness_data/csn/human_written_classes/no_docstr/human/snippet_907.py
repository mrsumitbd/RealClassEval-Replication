import copy

class Baseevents:

    def __init__(self):
        self.name = '?'
        self.datain = {}

    def input(self, data):
        r = copy.copy(data)
        del r['update-type']
        self.datain = r

    def __repr__(self):
        return u'<{} event ({})>'.format(self.name, self.datain)