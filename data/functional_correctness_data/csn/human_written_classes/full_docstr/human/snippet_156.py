class SimpleService:
    """Hold information about an access service enabled on a dataset.

    Attributes
    ----------
    name : str
        The name of the service
    service_type : str
        The service type (i.e. "OPENDAP", "NetcdfSubset", "WMS", etc.)
    access_urls : dict[str, str]
        A dictionary of access urls whose keywords are the access service
        types defined in the catalog (for example, "OPENDAP", "NetcdfSubset",
        "WMS", etc.)

    """

    def __init__(self, service_node):
        """Initialize the Dataset object.

        Parameters
        ----------
        service_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a service node

        """
        self.name = service_node.attrib['name']
        self.service_type = CaseInsensitiveStr(service_node.attrib['serviceType'])
        self.base = service_node.attrib['base']
        self.access_urls = {}

    def is_resolver(self):
        """Return whether the service is a resolver service."""
        return self.service_type == 'Resolver'