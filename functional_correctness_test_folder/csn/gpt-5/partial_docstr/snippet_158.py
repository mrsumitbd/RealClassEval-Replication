from __future__ import annotations

import json
from typing import Union, List, Any


class IEncoder:
    def fits(self, current_count: int, current_size: int, max_size: int, new_span: Union[str, bytes]) -> bool:
        if not isinstance(new_span, (str, bytes)):
            raise TypeError("new_span must be str or bytes")

        if max_size < 0 or current_count < 0 or current_size < 0:
            return False

        if isinstance(new_span, bytes):
            new_size = len(new_span)
        else:
            new_size = len(new_span.encode("utf-8"))

        # account for a single-byte separator (newline) if this won't be the first item
        sep_size = 1 if current_count > 0 else 0
        return (current_size + sep_size + new_size) <= max_size

    def encode_span(self, span: 'Span') -> Union[str, bytes]:
        # Prefer bytes if a clear bytes representation is available
        if hasattr(span, "to_bytes") and callable(getattr(span, "to_bytes")):
            res = span.to_bytes()
            if not isinstance(res, bytes):
                raise TypeError("to_bytes() must return bytes")
            return res

        if hasattr(span, "__bytes__"):
            res = bytes(span)  # type: ignore[arg-type]
            if not isinstance(res, bytes):
                raise TypeError("__bytes__ must return bytes")
            return res

        # Next, try JSON/string encodings
        if hasattr(span, "to_json") and callable(getattr(span, "to_json")):
            res = span.to_json()
            if not isinstance(res, str):
                raise TypeError("to_json() must return str")
            return res

        if hasattr(span, "to_str") and callable(getattr(span, "to_str")):
            res = span.to_str()
            if not isinstance(res, str):
                raise TypeError("to_str() must return str")
            return res

        # Fallbacks: dict-like -> JSON string; else str()
        try:
            if hasattr(span, "to_dict") and callable(getattr(span, "to_dict")):
                as_dict = span.to_dict()
                return json.dumps(as_dict, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            pass

        if isinstance(span, (dict, list, tuple)):
            return json.dumps(span, separators=(",", ":"), ensure_ascii=False)

        return str(span)

    def encode_queue(self, queue: List[Union[str, bytes]]) -> Union[str, bytes]:
        if not isinstance(queue, list):
            raise TypeError("queue must be a list")

        if not queue:
            return b""

        has_bytes = any(isinstance(item, bytes) for item in queue)
        has_str = any(isinstance(item, str) for item in queue)

        if not (has_bytes or has_str):
            raise TypeError("queue must contain str or bytes items")

        if has_bytes and has_str:
            raise TypeError("queue contains a mix of str and bytes")

        if has_bytes:
            # join bytes with newline
            for item in queue:
                if not isinstance(item, bytes):
                    raise TypeError(
                        "All items must be bytes when queue is bytes")
            return b"\n".join(queue)

        # join strings with newline
        for item in queue:
            if not isinstance(item, str):
                raise TypeError("All items must be str when queue is str")
        return "\n".join(queue)
