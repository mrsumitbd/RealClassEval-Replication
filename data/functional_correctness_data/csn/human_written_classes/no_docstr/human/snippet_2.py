from typing import Optional

class _AccountDescriptor:

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls) -> Optional[str]:
        return obj._account_data.get(self.name)

    def __set__(self, obj, value) -> None:
        raise AttributeError('Cannot set readonly attribute')