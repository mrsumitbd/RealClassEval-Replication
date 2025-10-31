
class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        pass

    def encode_span(self, span: Span) -> Union[str, bytes]:
        '''Encodes a single span.
        :param span: Span object representing the span.
        :type span: Span
        :return: encoded span.
        :rtype: str or bytes
        '''
        pass

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        pass
