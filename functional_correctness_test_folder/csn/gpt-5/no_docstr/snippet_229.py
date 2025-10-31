class PacketContext:

    def __init__(self, packet):
        self.packet = packet

    def __getitem__(self, name):
        value = self.packet
        parts = name.split(".") if isinstance(name, str) and name else [name]
        for part in parts:
            value = self._resolve(value, part)
        return value

    def _resolve(self, obj, key):
        if obj is None:
            raise KeyError(key)

        # numeric index if applicable
        idx = None
        if isinstance(key, str) and key.isdigit():
            idx = int(key)

        # mapping access
        if isinstance(obj, dict):
            if key in obj:
                return obj[key]
            if idx is not None and idx in obj:
                return obj[idx]

        # sequence/indexed access
        if idx is not None:
            try:
                return obj[idx]
            except Exception:
                pass

        # attribute access
        if isinstance(key, str) and hasattr(obj, key):
            return getattr(obj, key)

        # fallback to generic __getitem__
        try:
            return obj[key]
        except Exception:
            pass

        raise KeyError(key)
