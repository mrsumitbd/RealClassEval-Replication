import warnings

class _DummyLogger:

    def info(self, msg: str) -> None:
        print(msg)

    def warning(self, msg: str) -> None:
        warnings.warn(msg, stacklevel=3)