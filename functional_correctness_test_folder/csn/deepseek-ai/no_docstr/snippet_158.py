
from typing import Union, List
from dataclasses import dataclass


@dataclass
class Span:
    content: Union[str, bytes]
    count: int


class IEncoder:

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        pass

    def encode_span(self, span: Span) -> Union[str, bytes]:
        pass

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        pass
