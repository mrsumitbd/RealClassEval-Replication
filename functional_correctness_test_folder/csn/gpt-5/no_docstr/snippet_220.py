class RateLimitsInfo:
    def __init__(
        self,
        limit=None,
        remaining=None,
        reset=None,
        reset_after=None,
        retry_after=None,
        used=None,
        bucket=None,
        scope=None,
    ):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.reset_after = reset_after
        self.retry_after = retry_after
        self.used = used
        self.bucket = bucket
        self.scope = scope

    def __str__(self):
        parts = []
        parts.append(
            f"limit={self.limit}" if self.limit is not None else "limit=?")
        parts.append(
            f"remaining={self.remaining}" if self.remaining is not None else "remaining=?")
        parts.append(
            f"used={self.used}" if self.used is not None else "used=?")
        parts.append(
            f"reset={self.reset}" if self.reset is not None else "reset=?")
        parts.append(
            f"reset_after={self.reset_after}" if self.reset_after is not None else "reset_after=?")
        parts.append(
            f"retry_after={self.retry_after}" if self.retry_after is not None else "retry_after=?")
        parts.append(f"bucket={self.bucket}" if self.bucket else "bucket=?")
        parts.append(f"scope={self.scope}" if self.scope else "scope=?")
        return f"RateLimitsInfo({', '.join(parts)})"

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return cls()

        def get_first(d, keys, default=None):
            for k in keys:
                if k in d:
                    return d[k]
            return default

        def to_int(v):
            try:
                if v is None:
                    return None
                if isinstance(v, bool):
                    return int(v)
                if isinstance(v, (int,)):
                    return v
                if isinstance(v, float):
                    # Some sources provide reset as float seconds; keep int for epoch
                    return int(v)
                s = str(v).strip()
                if s == "":
                    return None
                return int(float(s))
            except Exception:
                return None

        def to_float(v):
            try:
                if v is None:
                    return None
                if isinstance(v, (int, float)):
                    return float(v)
                s = str(v).strip()
                if s == "":
                    return None
                return float(s)
            except Exception:
                return None

        limit = get_first(data, ("limit", "rate_limit",
                          "x-ratelimit-limit", "X-RateLimit-Limit"))
        remaining = get_first(data, ("remaining", "rate_remaining",
                              "x-ratelimit-remaining", "X-RateLimit-Remaining"))
        used = get_first(
            data, ("used", "x-ratelimit-used", "X-RateLimit-Used"))
        reset = get_first(data, ("reset", "x-ratelimit-reset",
                          "X-RateLimit-Reset", "reset_epoch"))
        reset_after = get_first(data, ("reset_after", "reset-after",
                                "x-ratelimit-reset-after", "X-RateLimit-Reset-After"))
        retry_after = get_first(
            data, ("retry_after", "retry-after", "Retry-After"))
        bucket = get_first(
            data, ("bucket", "x-ratelimit-bucket", "X-RateLimit-Bucket"))
        scope = get_first(
            data, ("scope", "x-ratelimit-scope", "X-RateLimit-Scope"))

        return cls(
            limit=to_int(limit),
            remaining=to_int(remaining),
            reset=to_int(reset),
            reset_after=to_float(reset_after),
            retry_after=to_float(retry_after),
            used=to_int(used),
            bucket=str(bucket) if bucket is not None else None,
            scope=str(scope) if scope is not None else None,
        )

    @classmethod
    def from_headers(cls, headers):
        if headers is None:
            return cls()

        # Normalize header dict to case-insensitive lookup
        class _H:
            def __init__(self, h):
                self._map = {}
                try:
                    items = h.items()
                except Exception:
                    # Fallback if not dict-like
                    try:
                        items = list(h)
                    except Exception:
                        items = []
                for k, v in items:
                    self._map[str(k).lower()] = v

            def get(self, key, default=None):
                return self._map.get(str(key).lower(), default)

        h = _H(headers)

        def to_int(v):
            try:
                if v is None:
                    return None
                if isinstance(v, bool):
                    return int(v)
                if isinstance(v, int):
                    return v
                if isinstance(v, float):
                    return int(v)
                s = str(v).strip()
                if s == "":
                    return None
                # Some providers send decimal strings; convert via float first
                return int(float(s))
            except Exception:
                return None

        def to_float(v):
            try:
                if v is None:
                    return None
                if isinstance(v, (int, float)):
                    return float(v)
                s = str(v).strip()
                if s == "":
                    return None
                return float(s)
            except Exception:
                return None

        limit = h.get(
            "x-ratelimit-limit") or h.get("ratelimit-limit") or h.get("rate-limit")
        remaining = h.get(
            "x-ratelimit-remaining") or h.get("ratelimit-remaining")
        used = h.get("x-ratelimit-used") or h.get("ratelimit-used")
        reset = h.get("x-ratelimit-reset") or h.get("ratelimit-reset")
        reset_after = h.get(
            "x-ratelimit-reset-after") or h.get("ratelimit-reset-after")
        retry_after = h.get("retry-after")
        bucket = h.get("x-ratelimit-bucket") or h.get("ratelimit-bucket")
        scope = h.get("x-ratelimit-scope") or h.get("ratelimit-scope")

        return cls(
            limit=to_int(limit),
            remaining=to_int(remaining),
            reset=to_int(reset),
            reset_after=to_float(reset_after),
            retry_after=to_float(retry_after),
            used=to_int(used),
            bucket=str(bucket) if bucket is not None else None,
            scope=str(scope) if scope is not None else None,
        )
