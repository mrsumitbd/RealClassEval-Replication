
import sys
import pickle
from typing import Any, Iterable, Optional, Union


class IJavaStreamParser:
    """
    API of the Java stream parser.

    This implementation uses Python's pickle module as a stand‑in for a
    Java serialization stream. It is intentionally simple and should
    be replaced with a proper Java stream parser if required.
    """

    def __init__(self, stream: Optional[Union[bytes, bytearray, memoryview, Iterable[bytes]]] = None):
        """
        Initialise the parser with an optional binary stream.

        Parameters
        ----------
        stream : Optional[Union[bytes, bytearray, memoryview, Iterable[bytes]]]
            A binary stream or an iterable of bytes. If None, sys.stdin.buffer
            is used.
        """
        if stream is None:
            self.stream = sys.stdin.buffer
        else:
            # If the stream is a bytes-like object, wrap it in a BytesIO
            if isinstance(stream, (bytes, bytearray, memoryview)):
                from io import BytesIO

                self.stream = BytesIO(stream)
            else:
                self.stream = stream

    def run(self) -> list[Any]:
        """
        Parses the input stream and returns a list of deserialized objects.

        Returns
        -------
        list[Any]
            A list containing all objects read from the stream.
        """
        objects = []
        while True:
            try:
                obj = self._read_content()
                if obj is None:
                    break
                objects.append(obj)
            except EOFError:
                break
            except pickle.UnpicklingError:
                # Stop on unpickling errors to avoid infinite loops
                break
        return objects

    def dump(self, content: Any) -> bytes:
        """
        Dumps the given object(s) to a bytes string using pickle.

        Parameters
        ----------
        content : Any
            The object to serialize.

        Returns
        -------
        bytes
            The pickled representation of the object.
        """
        return pickle.dumps(content)

    def _read_content(
        self,
        type_code: Optional[Any] = None,
        block_data: Optional[Any] = None,
        class_desc: Optional[Any] = None,
    ) -> Any:
        """
        Parses the next content from the stream.

        This method is a thin wrapper around pickle.load. The additional
        parameters are present for API compatibility with a more complex
        Java stream parser but are ignored in this simplified implementation.

        Parameters
        ----------
        type_code : Optional[Any]
            Ignored in this implementation.
        block_data : Optional[Any]
            Ignored in this implementation.
        class_desc : Optional[Any]
            Ignored in this implementation.

        Returns
        -------
        Any
            The next deserialized object from the stream.

        Raises
        ------
        EOFError
            If the end of the stream is reached.
        """
        return pickle.load(self.stream)
