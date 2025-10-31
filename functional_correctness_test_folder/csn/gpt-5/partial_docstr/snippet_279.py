import copy
import base64
import datetime
import decimal
import uuid
from collections.abc import Mapping, Sequence


class SearchDumperExt:
    _MARK = "__sde__"

    def dump(self, record, data):
        def _dump_value(v):
            if isinstance(v, datetime.datetime):
                return {self._MARK: "datetime", "v": v.isoformat()}
            if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime):
                return {self._MARK: "date", "v": v.isoformat()}
            if isinstance(v, datetime.time):
                return {self._MARK: "time", "v": v.isoformat()}
            if isinstance(v, decimal.Decimal):
                return {self._MARK: "decimal", "v": str(v)}
            if isinstance(v, uuid.UUID):
                return {self._MARK: "uuid", "v": str(v)}
            if isinstance(v, (bytes, bytearray)):
                return {self._MARK: "bytes", "v": base64.b64encode(bytes(v)).decode("ascii")}
            if isinstance(v, set):
                return {self._MARK: "set", "v": [_dump_value(i) for i in v]}
            if isinstance(v, tuple):
                return {self._MARK: "tuple", "v": [_dump_value(i) for i in v]}
            if isinstance(v, Mapping):
                # Avoid re-wrapping already dumped markers
                if set(v.keys()) == {self._MARK, "v"} and isinstance(v.get(self._MARK), str):
                    return {k: _dump_value(val) for k, val in v.items()}
                return {str(k): _dump_value(val) for k, val in v.items()}
            if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):
                return [_dump_value(i) for i in v]
            return v

        return _dump_value(copy.deepcopy(data))

    def load(self, data, record_cls):
        def _load_value(v):
            if isinstance(v, Mapping) and self._MARK in v and "v" in v and isinstance(v[self._MARK], str):
                t = v[self._MARK]
                val = v["v"]
                if t == "datetime":
                    return datetime.datetime.fromisoformat(val)
                if t == "date":
                    return datetime.date.fromisoformat(val)
                if t == "time":
                    return datetime.time.fromisoformat(val)
                if t == "decimal":
                    return decimal.Decimal(val)
                if t == "uuid":
                    return uuid.UUID(val)
                if t == "bytes":
                    return base64.b64decode(val.encode("ascii"))
                if t == "set":
                    return set(_load_value(i) for i in val)
                if t == "tuple":
                    return tuple(_load_value(i) for i in val)
                # Unknown type marker: fall-through to generic handling
            if isinstance(v, Mapping):
                return {k: _load_value(val) for k, val in v.items()}
            if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):
                return [_load_value(i) for i in v]
            return v

        return _load_value(data)
