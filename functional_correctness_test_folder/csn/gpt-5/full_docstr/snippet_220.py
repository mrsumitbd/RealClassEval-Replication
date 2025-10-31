import datetime
import time
from email.utils import parsedate_to_datetime


class RateLimitsInfo:
    '''Data for rate limits.'''

    __slots__ = (
        'limit',
        'remaining',
        'used',
        'reset_epoch',
        'reset_after',
        'retry_after',
        'resource',
        'bucket',
        'window',
        'raw',
    )

    def __init__(
        self,
        limit=None,
        remaining=None,
        used=None,
        reset_epoch=None,
        reset_after=None,
        retry_after=None,
        resource=None,
        bucket=None,
        window=None,
        raw=None,
    ):
        self.limit = limit
        self.remaining = remaining
        self.used = used
        self.reset_epoch = reset_epoch
        self.reset_after = reset_after
        self.retry_after = retry_after
        self.resource = resource
        self.bucket = bucket
        self.window = window
        self.raw = raw or {}

    def __str__(self):
        parts = []
        if self.limit is not None:
            parts.append(f"limit={self.limit}")
        if self.remaining is not None:
            parts.append(f"remaining={self.remaining}")
        if self.used is not None:
            parts.append(f"used={self.used}")
        if self.reset_epoch is not None:
            try:
                dt = datetime.datetime.utcfromtimestamp(int(self.reset_epoch))
                parts.append(f"reset_at={dt.isoformat()}Z")
            except Exception:
                parts.append(f"reset_epoch={self.reset_epoch}")
        if self.reset_after is not None:
            parts.append(f"reset_after={self.reset_after}s")
        if self.retry_after is not None:
            parts.append(f"retry_after={self.retry_after}s")
        if self.resource:
            parts.append(f"resource={self.resource}")
        if self.bucket:
            parts.append(f"bucket={self.bucket}")
        if self.window:
            parts.append(f"window={self.window}")
        return ", ".join(parts) if parts else "No rate limit data"

    @classmethod
    def from_dict(cls, data):
        '''Create RateLimitsInfo from a dictionary.'''
        if data is None:
            return cls(raw={})
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        def to_int(val):
            if val is None or val == "":
                return None
            try:
                return int(val)
            except Exception:
                try:
                    return int(float(val))
                except Exception:
                    return None

        def to_float(val):
            if val is None or val == "":
                return None
            try:
                return float(val)
            except Exception:
                return None

        # Normalize keys to lower without spaces/underscores/dashes
        norm = {}
        for k, v in data.items():
            nk = str(k).strip().lower().replace("-", "_").replace(" ", "_")
            norm[nk] = v

        # Gather values with common aliases
        limit = to_int(norm.get("limit") or norm.get("x_ratelimit_limit"))
        remaining = to_int(norm.get("remaining")
                           or norm.get("x_ratelimit_remaining"))
        used = to_int(norm.get("used") or norm.get("x_ratelimit_used"))
        reset_epoch = to_int(norm.get("reset") or norm.get(
            "reset_epoch") or norm.get("x_ratelimit_reset"))
        reset_after = to_float(norm.get("reset_after")
                               or norm.get("x_ratelimit_reset_after"))
        retry_after = to_float(norm.get("retry_after"))

        resource = norm.get("resource") or norm.get("x_ratelimit_resource")
        bucket = norm.get("bucket") or norm.get("x_ratelimit_bucket")
        window = norm.get("window") or norm.get(
            "period") or norm.get("interval")

        return cls(
            limit=limit,
            remaining=remaining,
            used=used,
            reset_epoch=reset_epoch,
            reset_after=reset_after,
            retry_after=retry_after,
            resource=resource,
            bucket=bucket,
            window=window,
            raw=dict(data),
        )

    @classmethod
    def from_headers(cls, headers):
        '''Create RateLimitsInfo from HTTP headers.'''
        if headers is None:
            return cls(raw={})
        # Support any mapping-like object
        try:
            items = headers.items()
        except Exception:
            raise TypeError("headers must be a mapping with .items()")

        # Normalize header keys to lowercase
        norm = {}
        for k, v in items:
            nk = str(k).strip().lower()
            norm[nk] = v

        def get_first(name):
            v = norm.get(name)
            # Some clients may join multiple header values with commas
            if isinstance(v, str) and "," in v and name != "date":
                # Take the first token for numeric fields
                parts = [p.strip() for p in v.split(",")]
                return parts[0] if parts else v
            return v

        def to_int(val):
            if val is None or val == "":
                return None
            try:
                return int(val)
            except Exception:
                try:
                    return int(float(val))
                except Exception:
                    return None

        def to_float(val):
            if val is None or val == "":
                return None
            try:
                return float(val)
            except Exception:
                return None

        limit = to_int(get_first("x-ratelimit-limit"))
        remaining = to_int(get_first("x-ratelimit-remaining"))
        used = to_int(get_first("x-ratelimit-used"))
        reset_epoch = to_int(get_first("x-ratelimit-reset"))
        reset_after = to_float(get_first("x-ratelimit-reset-after"))

        # Retry-After can be seconds or HTTP-date
        retry_after_val = get_first("retry-after")
        retry_after = None
        if retry_after_val is not None and retry_after_val != "":
            # Try numeric seconds first
            ra_seconds = to_float(retry_after_val)
            if ra_seconds is not None:
                retry_after = ra_seconds
            else:
                try:
                    dt = parsedate_to_datetime(retry_after_val)
                    if dt.tzinfo is None:
                        # Assume UTC if no tz info
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    delta = (dt - now).total_seconds()
                    retry_after = max(0.0, delta)
                except Exception:
                    retry_after = None

        resource = get_first("x-ratelimit-resource")
        bucket = get_first("x-ratelimit-bucket")
        window = get_first(
            "x-ratelimit-window") or get_first("ratelimit-window")

        return cls(
            limit=limit,
            remaining=remaining,
            used=used,
            reset_epoch=reset_epoch,
            reset_after=reset_after,
            retry_after=retry_after,
            resource=resource,
            bucket=bucket,
            window=window,
            raw=dict(headers),
        )
