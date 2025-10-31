import json

class StatusMessage:
    OperationId = None
    Database = None
    Table = None
    IngestionSourceId = None
    IngestionSourcePath = None
    RootActivityId = None
    _raw = None

    def __init__(self, s):
        self._raw = s
        o = json.loads(s)
        for key, value in o.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                except Exception:
                    pass

    def __str__(self):
        return '{}'.format(self._raw)

    def __repr__(self):
        return '{0.__class__.__name__}({0._raw})'.format(self)