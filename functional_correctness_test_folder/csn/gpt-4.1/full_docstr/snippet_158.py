
from typing import Union, List


class Span:
    '''Dummy Span class for demonstration purposes.'''

    def __init__(self, data):
        self.data = data


class IEncoder:
    '''Encoder interface.'''

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        '''Returns whether the new span will fit in the list.'''
        if isinstance(new_span, str):
            new_size = len(new_span.encode('utf-8'))
        else:
            new_size = len(new_span)
        return (current_size + new_size) <= max_size

    def encode_span(self, span: Span) -> Union[str, bytes]:
        '''Encodes a single span.'''
        # Example: encode as JSON string
        import json
        return json.dumps({'data': span.data})

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        '''Encodes a list of pre-encoded spans.'''
        # Example: join JSON strings with commas and wrap in brackets
        if not queue:
            return '[]'
        if isinstance(queue[0], bytes):
            # Assume bytes are utf-8 encoded JSON strings
            items = [item.decode('utf-8') for item in queue]
        else:
            items = queue
        return '[' + ','.join(items) + ']'
