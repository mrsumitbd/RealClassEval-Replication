class EchoFilter:
    """
    A logger filter primarily for use with `StreamTeeLogger`.  Adding an
    `EchoFilter` to a `StreamTeeLogger` instances allows control over which
    modules' print statements, for example, are output to stdout.

    For example, to allow only output from the 'foo' module to be printed to
    the console:

    >>> stdout_logger = logging.getLogger('stsci.tools.logutil.stdout')
    >>> stdout_logger.addFilter(EchoFilter(include=['foo']))

    Now only print statements in the 'foo' module (or any sub-modules if 'foo'
    is a package) are printed to stdout.   Any other print statements are just
    sent to the appropriate logger.

    Parameters
    ----------
    include : iterable
        Packages or modules to include in stream output.  If set, then only the
        modules listed here are output to the stream.

    exclude : iterable
        Packages or modules to be excluded from stream output.  If set then all
        modules except for those listed here are output to the stream.  If both
        ``include`` and ``exclude`` are provided, ``include`` takes precedence
        and ``exclude`` is ignored.
    """

    def __init__(self, include=None, exclude=None):
        self.include = set(include) if include is not None else include
        self.exclude = set(exclude) if exclude is not None else exclude

    def filter(self, record):
        if self.include is None and self.exclude is None or not hasattr(record, 'orig_name'):
            return True
        record_name = record.orig_name.split('.')
        while record_name:
            if self.include is not None:
                if '.'.join(record_name) in self.include:
                    return True
            elif self.exclude is not None:
                if '.'.join(record_name) not in self.exclude:
                    return True
                else:
                    break
            record_name.pop()
        record.echo = False
        return True