
class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        new_size = current_size + len(new_span)
        return new_size <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        if isinstance(span, str):
            return span.encode('utf-8')
        elif isinstance(span, bytes):
            return span
        else:
            raise TypeError("Span must be either str or bytes")

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        encoded_queue = b''.join(self.encode_span(span) for span in queue)
        return encoded_queue
