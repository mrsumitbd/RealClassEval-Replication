from typing import Any

class _DummyModule:

    def __init__(self, module: str) -> None:
        self.module = module

    def __getattr__(self, name: str) -> Any:
        raise ValueError(f"Module '{self.module}' is not installed.")