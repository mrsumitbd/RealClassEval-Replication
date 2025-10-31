class ReceiverSocketListener:
    """
    Base class for listener of a ReceiverSocketBase.
    """

    def on_data(self, data: bytes, current_time: float) -> None:
        raise NotImplementedError

    def on_periodic_callback(self, current_time: float) -> None:
        raise NotImplementedError