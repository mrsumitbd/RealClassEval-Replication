
from typing import Union, List


class IEncoder:
    """
    A simple encoder that works with strings and bytes.
    """

    def fits(self, current_count: int, current_size: int, max_size: int,
             new_span: Union[str, bytes]) -> bool:
        """
        Determine whether adding `new_span` to the current payload would exceed
        the maximum allowed size.

        :param current_count: Number of spans already in the payload (unused).
        :param current_size: Current size in bytes of the payload.
        :param max_size: Maximum allowed size in bytes.
        :param new_span: The new span to be added, as a string or bytes.
        :return: True if the new span can be added without exceeding `max_size`.
        """
        if isinstance(new_span, bytes):
            new_len = len(new_span)
        else:
            new_len = len(new_span.encode("utf-8"))
        return current_size + new_len <= max_size

    def encode_span(self, span) -> Union[str, bytes]:
        """
        Encode a single span. The default implementation simply returns the
        string representation of the span. Subclasses may override this method
        to provide custom encoding logic.

        :param span: Span object representing the span.
        :return: Encoded span as a string or bytes.
        """
        # Default: use the span's __str__ representation.
        return str(span)

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        """
        Encode a queue of spans. The default implementation concatenates all
        elements, converting strings to UTF‑8 encoded bytes.

        :param queue: List of encoded spans (strings or bytes).
        :return: Concatenated payload as bytes.
        """
        # Convert all items to bytes and concatenate.
        encoded_parts = []
        for item in queue:
            if isinstance(item, bytes):
                encoded_parts.append(item)
            else:
                encoded_parts.append(item.encode("utf-8"))
        return b"".join(encoded_parts)
