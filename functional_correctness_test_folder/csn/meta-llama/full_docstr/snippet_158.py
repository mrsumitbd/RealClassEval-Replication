
from typing import Union, List
from dataclasses import dataclass

# Assuming Span is a dataclass for simplicity


@dataclass
class Span:
    """Span object representing a span."""
    # Add relevant fields as per your requirements
    name: str
    # Add other fields as needed


class IEncoder:
    '''Encoder interface.'''

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        '''Returns whether the new span will fit in the list.
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
        '''
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
        '''Encodes a list of pre-encoded spans.
        :param queue: list of encoded spans.
        :type queue: list
        :return: encoded list, type depends on the encoding.
        :rtype: str or bytes
        '''
        pass


class JSONEncoder(IEncoder):
    '''JSON Encoder implementation.'''

    import json

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        new_size = current_size + len(new_span)
        return new_size <= max_size

    def encode_span(self, span: Span) -> str:
        return self.json.dumps(span.__dict__)

    def encode_queue(self, queue: List[Union[str, bytes]]) -> str:
        return self.json.dumps(queue)


class ProtoEncoder(IEncoder):
    '''Protobuf Encoder implementation.'''

    import span_pb2  # Assuming you have a protobuf definition in span.proto

    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        new_size = current_size + len(new_span)
        return new_size <= max_size

    def encode_span(self, span: Span) -> bytes:
        proto_span = self.span_pb2.Span()
        proto_span.name = span.name
        # Add other fields as needed
        return proto_span.SerializeToString()

    def encode_queue(self, queue: List[Union[str, bytes]]) -> bytes:
        proto_queue = self.span_pb2.SpanQueue()
        for span in queue:
            proto_span = proto_queue.spans.add()
            proto_span.ParseFromString(span)
        return proto_queue.SerializeToString()


# Example usage
if __name__ == "__main__":
    span = Span("example_span")
    json_encoder = JSONEncoder()
    proto_encoder = ProtoEncoder()

    encoded_span_json = json_encoder.encode_span(span)
    print(f"JSON encoded span: {encoded_span_json}")

    encoded_span_proto = proto_encoder.encode_span(span)
    print(f"Protobuf encoded span: {encoded_span_proto}")

    queue = [encoded_span_json, encoded_span_json]
    encoded_queue_json = json_encoder.encode_queue(queue)
    print(f"JSON encoded queue: {encoded_queue_json}")

    queue_proto = [encoded_span_proto, encoded_span_proto]
    encoded_queue_proto = proto_encoder.encode_queue(queue_proto)
    print(f"Protobuf encoded queue: {encoded_queue_proto}")
