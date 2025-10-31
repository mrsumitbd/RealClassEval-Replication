
class SystemFieldContext:

    def __init__(self, field, record_cls):
        self._field = field
        self._record_cls = record_cls

    @property
    def field(self):
        return self._field

    @property
    def record_cls(self):
        return self._record_cls
