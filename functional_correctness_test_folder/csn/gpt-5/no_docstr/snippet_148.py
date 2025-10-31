class Addr:
    import time as _time

    def __init__(self, map):
        self._store = {}
        self.map = {}
        if map:
            if hasattr(map, "items"):
                items = map.items()
            else:
                items = map
            now = self._time.time()
            for k, v in items:
                if isinstance(v, tuple) and len(v) == 2:
                    val, t = v
                    exp_at = self._compute_expire_at(now, t)
                    self._store[k] = (val, exp_at)
                else:
                    self._store[k] = (v, None)
        self._refresh_visible()

    def update(self, *args):
        if not args:
            return
        now = self._time.time()
        data = {}
        # Support dict/update semantics: update(mapping), update(iterable), update(mapping, **kwargs), update(**kwargs)
        if len(args) == 1:
            src = args[0]
            if hasattr(src, "items"):
                data.update(src.items())
            else:
                for k, v in src:
                    data[k] = v
        elif len(args) >= 2:
            # First positional must be mapping
            src = args[0]
            if hasattr(src, "items"):
                data.update(src.items())
            else:
                for k, v in src:
                    data[k] = v
            # Remaining arguments are treated as kwargs-like mappings
            for extra in args[1:]:
                if hasattr(extra, "items"):
                    data.update(extra.items())
                else:
                    for k, v in extra:
                        data[k] = v

        for k, v in data.items():
            if isinstance(v, tuple) and len(v) == 2:
                val, t = v
                exp_at = self._compute_expire_at(now, t)
                self._store[k] = (val, exp_at)
            else:
                self._store[k] = (v, None)
        self._expire()

    def _expire(self):
        now = self._time.time()
        expired_keys = []
        for k, (_, exp_at) in self._store.items():
            if exp_at is not None and exp_at <= now:
                expired_keys.append(k)
        for k in expired_keys:
            self._store.pop(k, None)
        self._refresh_visible()
        return len(expired_keys)

    def _refresh_visible(self):
        now = self._time.time()
        self.map = {k: v for k, (v, exp_at) in self._store.items(
        ) if exp_at is None or exp_at > now}

    @staticmethod
    def _compute_expire_at(now, t):
        if t is None:
            return None
        # If t looks like absolute epoch (significantly larger than reasonable TTL), accept as absolute
        # Otherwise treat as relative ttl seconds
        try:
            t = float(t)
        except (TypeError, ValueError):
            return None
        # Heuristic threshold: if t is in the far past or > year 2286, treat as ttl anyway
        if t > 10_000_000:  # absolute epoch heuristic
            return t
        return now + t
