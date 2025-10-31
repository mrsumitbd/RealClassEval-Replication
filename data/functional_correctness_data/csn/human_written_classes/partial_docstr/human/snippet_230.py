class ExceptionCounterByType:
    """A context manager that counts exceptions by type.

    Exceptions increment the provided counter, whose last label's name
    must match the `type_label` argument.

    In other words:

    c = Counter('http_request_exceptions_total', 'Counter of exceptions',
                ['method', 'type'])
    with ExceptionCounterByType(c, extra_labels={'method': 'GET'}):
        handle_get_request()
    """

    def __init__(self, counter, type_label='type', extra_labels=None):
        self._counter = counter
        self._type_label = type_label
        self._labels = dict(extra_labels)

    def __enter__(self):
        pass

    def __exit__(self, typ, value, traceback):
        if typ is not None:
            self._labels.update({self._type_label: typ.__name__})
            self._counter.labels(**self._labels).inc()