class CompoundService:
    """Hold information about compound services.

    Attributes
    ----------
    name : str
        The name of the compound service
    service_type : str
        The service type (for this object, service type will always be
        "COMPOUND")
    services : list[SimpleService]
        A list of :class:`SimpleService` objects

    """

    def __init__(self, service_node):
        """Initialize a :class:`CompoundService` object.

        Parameters
        ----------
        service_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a compound service node

        """
        self.name = service_node.attrib['name']
        self.service_type = CaseInsensitiveStr(service_node.attrib['serviceType'])
        self.base = service_node.attrib['base']
        services = []
        subservices = 0
        for child in list(service_node):
            services.append(SimpleService(child))
            subservices += 1
        self.services = services
        self.number_of_subservices = subservices

    def is_resolver(self):
        """Return whether the service is a resolver service.

        For a compound service, this is always False because it will never be
        a resolver.
        """
        return False