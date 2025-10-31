class Event:
    """A read-only object representing a received event.

    The values of the evented variables can be accessed via the ``variables``
    dict, or as attributes on the instance itself. You should treat all
    attributes as read-only.

    Args:
        sid (str): the subscription id.
        seq (str): the event sequence number for that subscription.
        timestamp (str): the time that the event was received (from Python's
            `time.time` function).
        service (str): the service which is subscribed to the event.
        variables (dict, optional): contains the ``{names: values}`` of the
            evented variables. Defaults to `None`. The values may be
            `SoCoFault` objects if the metadata could not be parsed.

    Raises:
        AttributeError:  Not all attributes are returned with each event. An
            `AttributeError` will be raised if you attempt to access as an
            attribute a variable which was not returned in the event.

    Example:

        >>> print event.variables['transport_state']
        'STOPPED'
        >>> print event.transport_state
        'STOPPED'

    """

    def __init__(self, sid, seq, service, timestamp, variables=None):
        self.__dict__['sid'] = sid
        self.__dict__['seq'] = seq
        self.__dict__['timestamp'] = timestamp
        self.__dict__['service'] = service
        self.__dict__['variables'] = variables if variables is not None else {}

    def __getattr__(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise AttributeError('No such attribute: %s' % name)

    def __setattr__(self, name, value):
        """Disable (most) attempts to set attributes.

        This is not completely foolproof. It just acts as a warning! See
        `object.__setattr__`.
        """
        raise TypeError('Event object does not support attribute assignment')