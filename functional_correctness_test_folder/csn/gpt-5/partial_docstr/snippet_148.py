class Addr:

    def __init__(self, map):
        '''
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        '''
        self._map = map
        self.address = None
        self.value = None
        self.expires_at = None
        self._timer = None

    def _cancel_timer(self):
        t = self._timer
        self._timer = None
        if t is None:
            return
        # Support Twisted's DelayedCall or any object with cancel()
        cancel = getattr(t, "cancel", None)
        if callable(cancel):
            try:
                cancel()
            except Exception:
                pass

    def _schedule_expiry(self, seconds):
        self._cancel_timer()
        if seconds is None:
            self.expires_at = None
            return
        if seconds <= 0:
            self.expires_at = None
            self._expire()
            return
        self.expires_at = self._now() + seconds
        # Try map-like schedulers in order
        scheduler = None
        for name in ("callLater", "call_later", "schedule", "schedule_later"):
            scheduler = getattr(self._map, name, None)
            if callable(scheduler):
                break
        if scheduler is None:
            # Fallback: try to use reactor from map
            reactor = getattr(self._map, "reactor", None)
            scheduler = getattr(reactor, "callLater",
                                None) if reactor else None
        if callable(scheduler):
            try:
                self._timer = scheduler(seconds, self._expire)
                return
            except Exception:
                self._timer = None
        # If no scheduler available, expire immediately at least
        self._expire()

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        data = {}
        positional_value = None

        # Helper to coerce values
        def _to_int(v):
            try:
                return int(v)
            except Exception:
                try:
                    return int(float(v))
                except Exception:
                    return None

        # Parse various arg formats:
        for a in args:
            if isinstance(a, dict):
                for k, v in a.items():
                    data[str(k).upper()] = v
            elif isinstance(a, (tuple, list)) and len(a) == 2:
                k, v = a
                data[str(k).upper()] = v
            elif isinstance(a, str):
                if "=" in a:
                    k, v = a.split("=", 1)
                    data[str(k).upper()] = v
                else:
                    # Single string could be the value/target
                    positional_value = a
            else:
                # Fallback: treat as positional value if nothing else provided
                if positional_value is None:
                    positional_value = a

        # Extract fields commonly found in Tor ADDRMAP:
        # SOURCE address
        addr = data.get("ADDRESS") or data.get(
            "ADDR") or data.get("SRC") or data.get("SOURCE")
        if addr:
            self.address = addr

        # Target/new value mapping
        value = (
            data.get("VALUE") or data.get("TARGET") or data.get("NEW") or
            data.get("NEWADDR") or data.get("DST") or positional_value
        )
        if value is not None:
            self.value = value

        # Determine expiry seconds
        seconds = None

        # TTL in seconds
        ttl = data.get("TTL")
        if ttl is not None:
            seconds = _to_int(ttl)

        # EXPIRES as seconds from now
        exp = data.get("EXPIRES") or data.get("EXPIRY")
        if exp is not None:
            seconds = _to_int(exp)

        # Millisecond variations
        ttl_ms = data.get("TTL_MS")
        if ttl_ms is not None:
            ms = _to_int(ttl_ms)
            if ms is not None:
                seconds = ms / 1000.0

        exp_ms = data.get("EXPIRES_MS") or data.get("EXPIRY_MS")
        if exp_ms is not None:
            ms = _to_int(exp_ms)
            if ms is not None:
                seconds = ms / 1000.0

        # Absolute epoch expiry
        abs_exp = data.get("ABS_EXPIRES") or data.get(
            "ABS_EXPIRY") or data.get("EXPIRES_AT")
        if abs_exp is not None:
            ts = _to_int(abs_exp)
            if ts is not None:
                seconds = max(0, ts - self._now())

        # Cache permanence flags (no expiry)
        cache_flag = data.get("CACHE") or data.get(
            "CACHED") or data.get("PERMANENT") or data.get("NOEXPIRE")
        if isinstance(cache_flag, str):
            cache_flag = cache_flag.strip().upper() in ("1", "TRUE", "YES")
        if cache_flag:
            seconds = None

        # Schedule expiry based on determined seconds
        self._schedule_expiry(seconds)

        # Notify map of update
        self._notify_map_update()

        return self

    def _expire(self):
        '''
        callback done via callLater
        '''
        self._timer = None
        self.expires_at = None
        # Notify map about expiry, and allow map to remove/usurp this Addr
        notified = False
        for name in ("on_addr_expire", "addr_expired", "expire_addr", "expire", "remove"):
            fn = getattr(self._map, name, None)
            if callable(fn):
                try:
                    # Prefer remove by address if we have it
                    if name == "remove":
                        if self.address is not None:
                            fn(self.address)
                        else:
                            fn(self)
                    else:
                        fn(self)
                    notified = True
                    break
                except Exception:
                    # Try next handler if one fails
                    continue
        # If no map handler, just clear the value
        if not notified:
            self.value = None

    def _notify_map_update(self):
        for name in ("on_addr_update", "addr_updated", "update_addr", "updated", "update"):
            fn = getattr(self._map, name, None)
            if callable(fn):
                try:
                    fn(self)
                    return
                except Exception:
                    continue

    @staticmethod
    def _now():
        import time
        return time.time()
