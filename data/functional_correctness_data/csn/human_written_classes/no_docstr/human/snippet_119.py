import json
from skydive.encoder import JSONEncoder

class SyncRequestMsg:

    def __init__(self, filter):
        self.filter = filter

    def repr_json(self):
        return {'GremlinFilter': self.filter}

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder)