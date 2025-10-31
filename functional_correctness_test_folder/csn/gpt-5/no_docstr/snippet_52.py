class BitField:

    def __init__(self, *names):
        if not names:
            raise ValueError("At least one bit name is required")
        seen = set()
        cleaned = []
        for n in names:
            if not isinstance(n, str) or not n:
                raise TypeError("Bit names must be non-empty strings")
            if not n.isidentifier():
                raise ValueError(f"Invalid identifier for bit name: {n!r}")
            if n in seen:
                raise ValueError(f"Duplicate bit name: {n!r}")
            seen.add(n)
            cleaned.append(n)
        self._names = tuple(cleaned)
        self._bits = {name: 1 << i for i, name in enumerate(self._names)}

    def __call__(self, val):
        if not isinstance(val, int):
            raise TypeError("Value must be an integer bitmask")
        if val < 0:
            raise ValueError("Bitmask must be non-negative")
        # build an object with attributes per bit name
        # using a simple, lightweight object

        class _Flags:
            __slots__ = tuple(self._names) + ("__value__",)
        flags = _Flags()
        for name, bit in self._bits.items():
            setattr(flags, name, bool(val & bit))
        setattr(flags, "__value__", val)
        return flags
