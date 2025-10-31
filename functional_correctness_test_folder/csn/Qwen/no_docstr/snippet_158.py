
from typing import Union, List


class Span:
    def __init__(self, content: Union[str, bytes]):
        self.content = content


class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        return current_size + len(new_span) <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        return span.content

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        if all(isinstance(item, str) for item in queue):
            return ''.join(queue)
        elif all(isinstance(item, bytes) for item in queue):
            return b''.join(queue)
        else:
            raise ValueError(
                "Queue must contain either all strings or all bytes")
