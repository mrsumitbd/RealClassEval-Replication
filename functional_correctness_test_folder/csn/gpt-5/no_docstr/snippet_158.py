from typing import Union, List, Any


class IEncoder:
    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        if not isinstance(new_span, (str, bytes)):
            raise TypeError("new_span must be str or bytes")
        sep_len = 1 if current_count > 0 else 0
        try:
            new_len = len(new_span)
        except Exception:
            new_len = len(str(new_span))
        return (current_size + sep_len + new_len) <= max_size

    def encode_span(self, span: Any) -> Union[str, bytes]:
        if isinstance(span, (str, bytes)):
            return span
        if hasattr(span, "__bytes__"):
            try:
                return bytes(span)
            except Exception:
                pass
        to_bytes = getattr(span, "to_bytes", None)
        if callable(to_bytes):
            try:
                b = to_bytes()
                if isinstance(b, (bytes, bytearray)):
                    return bytes(b)
            except Exception:
                pass
        b_attr = getattr(span, "bytes", None)
        if isinstance(b_attr, (bytes, bytearray)):
            return bytes(b_attr)
        text_attr = getattr(span, "text", None)
        if isinstance(text_attr, str):
            return text_attr
        content_attr = getattr(span, "content", None)
        if isinstance(content_attr, (str, bytes, bytearray)):
            return content_attr if isinstance(content_attr, str) else bytes(content_attr)
        return str(span)

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        if not queue:
            return b""
        has_str = any(isinstance(x, str) for x in queue)
        has_bytes = any(isinstance(x, (bytes, bytearray)) for x in queue)
        if has_str and has_bytes:
            raise TypeError("Mixed str and bytes are not supported")
        if has_bytes:
            return b"".join(x if isinstance(x, (bytes, bytearray)) else bytes(x) for x in queue)
        return "".join(x if isinstance(x, str) else x.decode("utf-8", "replace") for x in queue)
