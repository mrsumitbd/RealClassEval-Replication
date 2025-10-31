import inspect

class StreamSink:
    """A sink that writes log messages to a stream object.

    Parameters
    ----------
    stream
        A stream object that supports write operations.
    """

    def __init__(self, stream):
        self._stream = stream
        self._flushable = callable(getattr(stream, 'flush', None))
        self._stoppable = callable(getattr(stream, 'stop', None))
        self._completable = inspect.iscoroutinefunction(getattr(stream, 'complete', None))

    def write(self, message):
        """Write a message to the stream.

        Parameters
        ----------
        message
            The message to write.
        """
        self._stream.write(message)
        if self._flushable:
            self._stream.flush()

    def stop(self):
        """Stop the stream if it supports the stop operation."""
        if self._stoppable:
            self._stream.stop()

    def tasks_to_complete(self):
        """Return list of tasks that need to be completed.

        Returns
        -------
        list
            List of tasks to complete.
        """
        if not self._completable:
            return []
        return [self._stream.complete()]