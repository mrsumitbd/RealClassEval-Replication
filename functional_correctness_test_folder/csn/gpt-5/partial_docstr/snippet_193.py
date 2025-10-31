class CkClass:
    def flags2text(self):
        flags = getattr(self, 'flags', 0)
        fmap = getattr(self, 'flags_map', {})
        if not isinstance(flags, int) or not isinstance(fmap, dict) or not fmap:
            return str(flags)
        names = []
        remaining = flags
        # Sort masks descending to handle composite masks consistently
        for mask, name in sorted(fmap.items(), key=lambda kv: kv[0], reverse=True):
            if not isinstance(mask, int):
                continue
            if flags & mask == mask and mask != 0:
                names.append(str(name))
                remaining &= ~mask
        if remaining:
            names.append(hex(remaining))
        return ','.join(names)

    def state2text(self):
        state = getattr(self, 'state', None)
        smap = getattr(self, 'state_map', None)
        if isinstance(smap, dict) and state in smap:
            return str(smap[state])
        return str(state)

    def to_dict(self):
        def serialize(value):
            if isinstance(value, CkClass):
                return value.to_dict()
            if isinstance(value, dict):
                return {k: serialize(v) for k, v in value.items()}
            if isinstance(value, (list, tuple, set)):
                t = type(value)
                return [serialize(v) for v in value]
            return value

        out = {}
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            if callable(v):
                continue
            out[k] = serialize(v)
        return out

    def __str__(self):
        items = []
        for k, v in self.to_dict().items():
            items.append(f"{k}={v!r}")
        return f"{self.__class__.__name__}(" + ", ".join(items) + ")"
