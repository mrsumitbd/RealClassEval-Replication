
from dataclasses import dataclass, fields


@dataclass
class OverridableConfig:
    def __post_init__(self) -> None:
        self._overridden_fields = set()
        self._default_values = {field.name: getattr(
            self, field.name) for field in fields(self)}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if key not in [field.name for field in fields(self)]:
            raise ValueError(f"Invalid key: {key}")

        if reset_to_defaults:
            setattr(self, key, self._default_values[key])

        self._overridden_fields.add(key)
