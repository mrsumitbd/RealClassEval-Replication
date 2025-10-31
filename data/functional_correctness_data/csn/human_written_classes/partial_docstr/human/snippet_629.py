from typing import Any

class _MocketSSLContext:
    """For Python 3.6 and newer."""

    class FakeSetter(int):

        def __set__(self, *args: Any) -> None:
            pass
    minimum_version = FakeSetter()
    options = FakeSetter()
    verify_mode = FakeSetter()
    verify_flags = FakeSetter()