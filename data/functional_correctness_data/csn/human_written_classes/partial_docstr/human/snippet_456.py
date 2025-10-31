from typing import Union, Optional, Any, AnyStr, overload, cast
import io

class TextBufferIO(io.TextIOWrapper):
    """Stream class that handles Python string contents for files."""

    def __init__(self, contents: Optional[bytes]=None, newline: Optional[str]=None, encoding: Optional[str]=None, errors: str='strict'):
        self._bytestream = io.BytesIO(contents or b'')
        super().__init__(self._bytestream, encoding=encoding, errors=errors, newline=newline)

    def getvalue(self) -> bytes:
        return self._bytestream.getvalue()

    def putvalue(self, value: bytes) -> None:
        self._bytestream.write(value)