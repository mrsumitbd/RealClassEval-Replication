class OmniRealtimeCallback:
    """
    An interface that defines callback methods for getting omni-realtime results. # noqa E501
    Derive from this class and implement its function to provide your own data.
    """

    def on_open(self) -> None:
        pass

    def on_close(self, close_status_code, close_msg) -> None:
        pass

    def on_event(self, message: str) -> None:
        pass