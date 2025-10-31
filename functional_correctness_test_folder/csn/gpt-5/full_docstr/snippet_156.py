class SimpleService:
    '''Hold information about an access service enabled on a dataset.
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
    '''

    def __init__(self, service_node):
        '''Initialize the Dataset object.
        Parameters
        ----------
        service_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a service node
        '''
        if service_node is None:
            raise ValueError(
                "service_node must be an xml.etree.ElementTree.Element")

        attrs = service_node.attrib or {}

        # Extract name
        self.name = attrs.get('name') or attrs.get('id') or ''

        # Extract service type (normalize to preserve original but provide consistent checks)
        st = (
            attrs.get('serviceType')
            or attrs.get('type')
            or attrs.get('service_type')
            or ''
        )
        self.service_type = st if isinstance(st, str) else str(st)

        # Try to determine a base/url for this service
        base = (
            attrs.get('base')
            or attrs.get('url')
            or attrs.get('href')
        )
        if base is None:
            # Attempt to find any attribute that ends with 'href' (namespaced or not)
            for k, v in attrs.items():
                if k.lower().endswith('href'):
                    base = v
                    break

        # Build access_urls dict keyed by service_type when we have both
        self.access_urls = {}
        if self.service_type:
            # If base is missing, leave dict empty; otherwise add mapping
            if base:
                self.access_urls[self.service_type] = base

    def is_resolver(self):
        '''Return whether the service is a resolver service.'''
        st = (self.service_type or '').strip().lower()
        return st == 'resolver'
