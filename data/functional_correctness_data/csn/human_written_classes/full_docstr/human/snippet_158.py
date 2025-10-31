from typing import Union
from py_zipkin.encoding._helpers import Span
from typing import List

class IEncoder:
    """Encoder interface."""

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        """Returns whether the new span will fit in the list.

        :param current_count: number of spans already in the list.
        :type current_count: int
        :param current_size: sum of the sizes of all the spans already in the list.
        :type current_size: int
        :param max_size: max supported transport payload size.
        :type max_size: int
        :param new_span: encoded span object that we want to add the the list.
        :type new_span: str or bytes
        :return: True if the new span can be added to the list, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError()

    def encode_span(self, span: Span) -> Union[str, bytes]:
        """Encodes a single span.

        :param span: Span object representing the span.
        :type span: Span
        :return: encoded span.
        :rtype: str or bytes
        """
        raise NotImplementedError()

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        """Encodes a list of pre-encoded spans.

        :param queue: list of encoded spans.
        :type queue: list
        :return: encoded list, type depends on the encoding.
        :rtype: str or bytes
        """
        raise NotImplementedError()