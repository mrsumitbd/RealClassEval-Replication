from binascii import hexlify
import struct
import attr

@attr.define
class _ReprRequest:
    """
    Wrapper for request `bytes` that gives it a comprehensible repr for use in
    log messages.

    >>> _ReprRequest(b'\x00\x02\x00\x00\x00\x00\x00ÿ')
    ListOffsetsRequest0 correlationId=16 (8 bytes)
    """
    _request: bytes = attr.ib()
    _REQUEST_HEADER = struct.Struct('>hhi')

    def __attrs_post_init__(self):
        if not isinstance(self._request, bytes):
            raise TypeError(f'request must be bytes, not {type(self._request).__name__}')

    def __str__(self):
        length = len(self._request)
        if length < 8:
            return f"invalid request ({hexlify(self._request).decode('ascii')})"
        key, version, correlation_id = self._REQUEST_HEADER.unpack_from(self._request)
        try:
            key_name = KafkaCodec.key_name(key)
        except KeyError:
            return f'request key={key}v{version} correlationId={correlation_id} ({length:,d} bytes)'
        return f'{key_name}Request{version} correlationId={correlation_id} ({length:,d} bytes)'