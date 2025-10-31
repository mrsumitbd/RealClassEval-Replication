class AccessEnumMixin:
    @classmethod
    def validate(cls, level):
        if isinstance(level, cls):
            return level

        # Try by direct value match
        for member in cls:
            if level == member.value:
                return member

        # Try by name or value as string (case-insensitive)
        if isinstance(level, str):
            lvl = level.strip()
            # by name
            for member in cls:
                if member.name.lower() == lvl.lower():
                    return member
            # by value string
            for member in cls:
                if str(member.value).lower() == lvl.lower():
                    return member

        valid = ", ".join(
            [f"{m.name}({m.value})" for m in cls]
        )
        raise ValueError(f"Invalid level: {level!r}. Expected one of: {valid}")

    def __str__(self):
        return str(self.value)
