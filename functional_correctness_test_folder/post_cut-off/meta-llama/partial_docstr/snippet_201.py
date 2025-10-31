
from dataclasses import dataclass, fields

# Assuming OverrideRegistry is defined elsewhere


class OverrideRegistry:
    overrides = {}

    @classmethod
    def register(cls, key, override_values):
        cls.overrides[key] = override_values

    @classmethod
    def get_override(cls, key):
        return cls.overrides.get(key, {})


@dataclass
class OverridableConfig:
    def __post_init__(self) -> None:
        self._override_key = 'default'
        self.set_override(self._override_key)

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        override_values = OverrideRegistry.get_override(key)
        for field in fields(self):
            if field.name.startswith('_'):
                continue
            if override_values and field.name in override_values:
                setattr(self, field.name, override_values[field.name])
            elif reset_to_defaults:
                setattr(self, field.name, field.default)
        self._override_key = key


# Example usage:
OverrideRegistry.register('default', {})
OverrideRegistry.register('custom', {'attr1': 'custom_value'})


@dataclass
class MyConfig(OverridableConfig):
    attr1: str = 'default_value'
    attr2: int = 10


config = MyConfig()
print(config.attr1)  # Output: 'default_value'
config.set_override('custom')
print(config.attr1)  # Output: 'custom_value'
