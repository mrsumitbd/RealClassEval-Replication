from typing import Optional

class DeviceAffinity:
    """This is used to provide device affinities to exported function arguments."""

    def __init__(self, ordinal: int, queues: Optional[list]=None):
        self.ordinal = ordinal
        self.queues = queues

    def __eq__(self, other) -> bool:
        if not isinstance(other, DeviceAffinity):
            return False
        return self.ordinal == other.ordinal and self.queues == other.queues

    def __repr__(self) -> str:
        if self.queues is None:
            return f'DeviceAffinity({self.ordinal})'
        return f"DeviceAffinity({self.ordinal}, [{', '.join(self.queues)}])"