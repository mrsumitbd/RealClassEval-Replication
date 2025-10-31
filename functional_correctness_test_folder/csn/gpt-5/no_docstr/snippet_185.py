class Transport:

    def __init__(self):
        self._open = False
        self._conn_info = None
        self._sequence = 0
        self._history = []

    def open(self, request):
        if self._open:
            return False
        self._conn_info = request
        self._open = True
        return True

    def send(self, request):
        if not self._open:
            raise RuntimeError("Transport is not open")
        self._sequence += 1
        record = {
            "sequence": self._sequence,
            "request": request,
            "connection": self._conn_info,
        }
        self._history.append(record)
        return {
            "status": "ok",
            "sequence": self._sequence,
            "request": request,
            "connection": self._conn_info,
        }
