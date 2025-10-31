class ResultCallback:
    """
    An interface that defines callback methods for getting speech synthesis results. # noqa E501
    Derive from this class and implement its function to provide your own data.
    """

    def on_open(self) -> None:
        pass

    def on_complete(self) -> None:
        pass

    def on_error(self, message) -> None:
        pass

    def on_close(self) -> None:
        pass

    def on_event(self, message: str) -> None:
        pass

    def on_data(self, data: bytes) -> None:
        pass