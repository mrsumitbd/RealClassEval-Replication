class Addr:
    '''
    One address mapping (e.g. example.com -> 127.0.0.1)
    '''

    def __init__(self, map):
        '''
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        '''
        self.map = map
        self.name = None
        self.mapped = None
        self.cached = False
        self.permanent = False
        self.unknown = False
        self.expires = None  # epoch seconds
        self._timer = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        # Flatten args to a simple list of tokens
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            tokens = list(args[0])
        else:
            tokens = list(args)

        if not tokens:
            return

        # Minimum expected: name [mapped]
        self.name = tokens[0] if len(tokens) >= 1 else self.name
        self.mapped = tokens[1] if len(tokens) >= 2 else self.mapped

        # Reset flags for a fresh update
        self.cached = False
        self.permanent = False
        self.unknown = False
        new_expires = None

        # Parse trailing flags/kv pairs
        for tok in tokens[2:]:
            if not isinstance(tok, str):
                continue
            up = tok.upper()
            if up == 'CACHED':
                self.cached = True
            elif up == 'NEVER':
                # Explicit never-expire
                self.permanent = True
                new_expires = None
            elif up == 'UNKNOWN':
                self.unknown = True
            elif up.startswith('EXPIRES='):
                val = tok.split('=', 1)[1]
                if val.upper() == 'NEVER':
                    self.permanent = True
                    new_expires = None
                else:
                    parsed = self._parse_expiry(val)
                    if parsed is not None:
                        new_expires = parsed

        # Apply expiry scheduling
        self._cancel_timer()

        if self.permanent:
            self.expires = None
            return

        if new_expires is not None:
            self.expires = new_expires
        # If no new expiry provided, retain current expires if any.

        if self.expires is not None:
            import time
            delay = max(0.0, self.expires - time.time())
            if delay == 0.0:
                self._expire()
            else:
                self._schedule_timer(delay)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self._cancel_timer()
        # On expiry, remove mapping and notify the map if possible
        if hasattr(self.map, 'remove') and self.name is not None:
            try:
                self.map.remove(self.name)
            except Exception:
                pass
        # Clear state
        self.mapped = None
        self.expires = None
        self.cached = False
        self.permanent = False
        self.unknown = False

    # Internal helpers

    def _parse_expiry(self, val):
        # Try UNIX epoch integer/float
        try:
            return float(val)
        except Exception:
            pass
        # Try ISO-like or Tor style "YYYY-MM-DD HH:MM:SS"
        from datetime import datetime, timezone
        fmts = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S%z",
        ]
        for fmt in fmts:
            try:
                dt = datetime.strptime(val, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.timestamp()
            except Exception:
                continue
        return None

    def _schedule_timer(self, delay):
        # Prefer map.callLater if available (Twisted-style), else fallback
        if hasattr(self.map, 'callLater') and callable(getattr(self.map, 'callLater')):
            try:
                self._timer = self.map.callLater(delay, self._expire)
                return
            except Exception:
                self._timer = None
        try:
            import threading
            t = threading.Timer(delay, self._expire)
            t.daemon = True
            t.start()
            self._timer = t
        except Exception:
            self._timer = None

    def _cancel_timer(self):
        if self._timer is None:
            return
        try:
            # Twisted-style DelayedCall
            if hasattr(self._timer, 'active') and self._timer.active():
                self._timer.cancel()
            # threading.Timer
            elif hasattr(self._timer, 'cancel'):
                self._timer.cancel()
        except Exception:
            pass
        finally:
            self._timer = None
