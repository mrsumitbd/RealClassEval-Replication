
class _AddressListener:
    """
    A simple address listener that keeps track of service addresses.
    The listener expects the subscriber to call `handle_msg` whenever a
    new address message is received.  Messages are expected to be
    dictionaries containing at least the keys 'service', 'address',
    and optionally 'port'.
    """

    def __init__(self, subscriber, services='', nameserver='localhost'):
        """
        Initialize the address listener.

        Parameters
        ----------
        subscriber : object
            The object that will deliver messages to this listener.
            It is stored for potential future use but not required
            to have any specific interface.
        services : str, optional
            A comma‑separated list of service names to filter on.
            If empty, all services are accepted.
        nameserver : str, optional
            The hostname of the nameserver to use for reverse lookups.
            Default is 'localhost'.
        """
        self.subscriber = subscriber
        self.services = set(s.strip()
                            for s in services.split(',') if s.strip())
        self.nameserver = nameserver
        self._addresses = {}  # service -> list of (address, port) tuples

    def handle_msg(self, msg):
        """
        Handle an incoming message.

        Parameters
        ----------
        msg : dict
            The message dictionary.  Expected keys are:
            - 'service': the name of the service
            - 'address': the IP address or hostname
            - 'port': (optional) the port number
            - 'ttl': (optional) time‑to‑live in seconds

        The message is stored in the internal address table if it
        matches the configured service filter.
        """
        if not isinstance(msg, dict):
            return

        service = msg.get('service')
        address = msg.get('address')
        port = msg.get('port', None)

        if not service or not address:
            return

        # Filter by service if a filter is set
        if self.services and service not in self.services:
            return

        entry = (address, port)
        self._addresses.setdefault(service, []).append(entry)

    def get_addresses(self, service=None):
        """
        Retrieve stored addresses.

        Parameters
        ----------
        service : str, optional
            If provided, return the list of addresses for that service.
            If omitted, return the entire address mapping.

        Returns
        -------
        dict or list
            The address mapping or the list of addresses for the
            specified service.
        """
        if service is None:
            return dict(self._addresses)
        return list(self._addresses.get(service, []))

    def __repr__(self):
        return (
            f"<_AddressListener services={sorted(self.services) or 'all'} "
            f"nameserver={self.nameserver!r} "
            f"addresses={len(self._addresses)}>"
        )
