class TraceId:

    def __init__(self):
        import secrets
        tid = secrets.token_hex(16)
        while tid == "0" * 32:
            tid = secrets.token_hex(16)
        self._id = tid

    def to_id(self):
        return self._id
