
from typing import Union, List


class Span:
    def __init__(self, value: Union[str, bytes]):
        self.value = value


class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        raise NotImplementedError("Subclass must implement fits method")

    def encode_span(self, span: Span) -> Union[str, bytes]:
        raise NotImplementedError("Subclass must implement encode_span method")

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        raise NotImplementedError(
            "Subclass must implement encode_queue method")


class StringEncoder(IEncoder):
    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        new_span_size = len(new_span)
        return current_size + new_span_size <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        return span.value

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        return ''.join(queue)


class BytesEncoder(IEncoder):
    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        if isinstance(new_span, str):
            new_span_size = len(new_span.encode())
        else:
            new_span_size = len(new_span)
        return current_size + new_span_size <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        if isinstance(span.value, str):
            return span.value.encode()
        else:
            return span.value

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        result = bytearray()
        for item in queue:
            if isinstance(item, str):
                result.extend(item.encode())
            else:
                result.extend(item)
        return bytes(result)


# Example usage
if __name__ == "__main__":
    span1 = Span("Hello")
    span2 = Span(b"World")

    string_encoder = StringEncoder()
    print(string_encoder.encode_span(span1))  # Output: Hello
    # Output: Hello World
    print(string_encoder.encode_queue(["Hello", " ", "World"]))

    bytes_encoder = BytesEncoder()
    print(bytes_encoder.encode_span(span2))  # Output: b'World'
    # Output: b'Hello World'
    print(bytes_encoder.encode_queue(["Hello", b" ", "World"]))
