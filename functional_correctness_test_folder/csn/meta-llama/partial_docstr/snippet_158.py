
from typing import Union, List


class Span:
    # Assuming Span is defined elsewhere, if not, you need to define it
    def __init__(self, start: int, end: int, text: str):
        self.start = start
        self.end = end
        self.text = text


class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        """Checks if adding a new span exceeds the maximum allowed size.

        :param current_count: The current number of spans.
        :type current_count: int
        :param current_size: The current total size of the encoded spans.
        :type current_size: int
        :param max_size: The maximum allowed total size.
        :type max_size: int
        :param new_span: The new span to be added, encoded.
        :type new_span: str or bytes
        :return: True if adding the new span doesn't exceed max_size, False otherwise.
        :rtype: bool
        """
        new_size = current_size + len(new_span)
        return new_size <= max_size

    def encode_span(self, span: 'Span') -> Union[str, bytes]:
        '''Encodes a single span.
        :param span: Span object representing the span.
        :type span: Span
        :return: encoded span.
        :rtype: str or bytes
        '''
        # For demonstration, let's assume we're encoding the span as a string
        # containing its start, end, and text.
        return f"{span.start}:{span.end}:{span.text}".encode('utf-8')

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        """Encodes a list of spans or already encoded spans into a single encoded output.

        :param queue: A list of spans or encoded spans to be encoded together.
        :type queue: List[str or bytes]
        :return: The encoded queue.
        :rtype: str or bytes
        """
        encoded_parts = []
        for item in queue:
            if isinstance(item, str):
                # If item is a string, encode it to bytes
                encoded_parts.append(item.encode('utf-8'))
            elif isinstance(item, bytes):
                # If item is already bytes, use it as is
                encoded_parts.append(item)
            else:
                raise ValueError("Queue items must be either str or bytes")

        # Concatenate all encoded parts
        if not encoded_parts:
            return b''  # or return '' depending on your requirements

        return b''.join(encoded_parts)


# Example usage
if __name__ == "__main__":
    encoder = IEncoder()
    span1 = Span(0, 5, "Hello")
    span2 = Span(6, 11, "World")

    encoded_span1 = encoder.encode_span(span1)
    encoded_span2 = encoder.encode_span(span2)

    print(f"Encoded Span 1: {encoded_span1}")
    print(f"Encoded Span 2: {encoded_span2}")

    queue = [encoded_span1, encoded_span2]
    encoded_queue = encoder.encode_queue(queue)
    print(f"Encoded Queue: {encoded_queue}")

    print(
        f"Fits in 100 bytes: {encoder.fits(2, len(encoded_queue), 100, encoded_span1)}")
