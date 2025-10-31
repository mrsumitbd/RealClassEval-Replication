
from typing import Union, List


class Span:
    def __init__(self, data):
        self.data = data


class IEncoder:
    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        if isinstance(new_span, str):
            new_size = len(new_span.encode('utf-8'))
        else:
            new_size = len(new_span)
        return (current_size + new_size) <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        # Example: encode as JSON string
        import json
        return json.dumps(span.data)

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        # Concatenate all spans as a single string separated by newlines
        if not queue:
            return ""
        if isinstance(queue[0], bytes):
            return b'\n'.join(queue)
        else:
            return '\n'.join(queue)
