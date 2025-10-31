from typing import Union, Optional, Any, AnyStr, overload, cast
import io

class BinaryBufferIO(io.BytesIO):
    """Stream class that handles byte contents for files."""

    def __init__(self, contents: Optional[bytes]):
        super().__init__(contents or b'')

    def putvalue(self, value: bytes) -> None:
        self.write(value)