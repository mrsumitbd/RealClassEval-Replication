class _ShutdownManager:

    def __init__(self, logger=None) -> None:
        raise NotImplementedError

    def add_notification(self) -> None:
        raise NotImplementedError

    def remove_notification(self) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        raise NotImplementedError