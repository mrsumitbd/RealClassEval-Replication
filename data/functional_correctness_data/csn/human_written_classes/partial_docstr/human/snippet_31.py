import logging

class StandardSink:
    """A sink that writes log messages using the standard logging module.

    Parameters
    ----------
    handler
        A logging handler instance.
    """

    def __init__(self, handler):
        self._handler = handler

    def write(self, message):
        """Write a message using the standard logging handler.

        Parameters
        ----------
        message
            The message to write.
        """
        raw_record = message.record
        message = str(message)
        exc = raw_record['exception']
        record = logging.getLogger().makeRecord(raw_record['name'], raw_record['level'].no, raw_record['file'].path, raw_record['line'], message, (), (exc.type, exc.value, exc.traceback) if exc else None, raw_record['function'], {'extra': raw_record['extra']})
        if exc:
            record.exc_text = '\n'
        record.levelname = raw_record['level'].name
        self._handler.handle(record)

    def stop(self):
        """Close the logging handler."""
        self._handler.close()

    def tasks_to_complete(self):
        """Return list of tasks that need to be completed.

        Returns
        -------
        list
            Empty list as standard sink has no async tasks.
        """
        return []