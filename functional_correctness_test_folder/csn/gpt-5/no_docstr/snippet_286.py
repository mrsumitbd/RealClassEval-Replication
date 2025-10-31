from enum import Enum


class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        if isinstance(level, cls):
            return level

        if isinstance(level, str):
            key = level.strip()

            # Exact name match
            if key in cls.__members__:
                return cls.__members__[key]

            # Case-insensitive name match
            for name, member in cls.__members__.items():
                if name.lower() == key.lower():
                    return member

            # Match by string value (case-insensitive)
            for member in cls:
                val = getattr(member, "value", None)
                if isinstance(val, str) and (val == key or val.lower() == key.lower()):
                    return member
        else:
            # Try to construct by value
            try:
                return cls(level)
            except Exception:
                pass

        allowed = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Invalid {cls.__name__}: {level!r}. Allowed: {allowed}")

    def __str__(self):
        name = getattr(self, "name", None)
        if isinstance(name, str):
            return name.lower()
        return str(getattr(self, "value", super().__str__()))
