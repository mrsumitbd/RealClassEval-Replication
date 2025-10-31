from typing_extensions import Self
import typing as t

class JSONRPCSettings:

    def __init__(self: Self, defaults: dict[str, t.Any] | None=None) -> None:
        self.defaults = defaults or DEFAULTS
        self.setup(self.defaults)

    def __getattr__(self: Self, attr: str) -> t.Any:
        if attr not in self.defaults:
            raise AttributeError(f'invalid setting: {attr!r}') from None
        val = self.defaults[attr]
        setattr(self, attr, val)
        return val

    def setup(self: Self, defaults: dict[str, t.Any]) -> None:
        for attr, val in defaults.items():
            setattr(JSONRPCSettings, attr, val)