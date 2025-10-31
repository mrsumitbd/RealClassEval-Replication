
from typing import Union, List, Any


class IEncoder:
    """
    A simple encoder that can check if a new span fits into a buffer,
    encode individual spans, and encode a queue of spans.
    """

    def fits(self, current_count: int, current_size: int, max_size: int,
             new_span: Union[str, bytes]) -> bool:
        """
        Determine whether adding `new_span` to the current buffer would exceed
        `max_size`. The `current_count` parameter is accepted for API
        compatibility but is not used in this implementation.
        """
        if isinstance(new_span, str):
            span_size = len(new_span.encode('utf-8'))
        else:
            span_size = len(new_span)
        return current_size + span_size <= max_size

    def encode_span(self, span: Any) -> Union[str, bytes]:
        """
        Encode a single span. If the span is a string, it is encoded to UTF‑8
        bytes. If it is already bytes, it is returned unchanged. For any
        other type, the string representation is encoded to UTF‑8 bytes.
        """
        if isinstance(span, str):
            return span.encode('utf-8')
        if isinstance(span, bytes):
            return span
        return str(span).encode('utf-8')

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        """
        Encode a list of spans. Each element is encoded using `encode_span`
        and the resulting bytes are concatenated with a newline separator.
        The final result is returned as bytes.
        """
        encoded_parts = [self.encode_span(item) for item in queue]
        return b'\n'.join(encoded_parts)
