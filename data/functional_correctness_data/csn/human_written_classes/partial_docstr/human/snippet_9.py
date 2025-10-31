from typing import TYPE_CHECKING, Optional

class _ScaleDescriptor:
    """Scale descriptor which validates scale."""

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls) -> Optional[float]:
        return obj._print_options.get(self.name)

    def __set__(self, obj, value) -> None:
        getattr(obj, '_validate_num_property')(self.name, value)
        if value < 0.1 or value > 2:
            raise ValueError('Value of scale should be between 0.1 and 2')
        obj._print_options[self.name] = value