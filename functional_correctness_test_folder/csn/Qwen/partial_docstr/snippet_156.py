
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
        self.name = service_node.get('name')
        self.service_type = service_node.get('service_type')
        self.access_urls = service_node.get('access_urls', {})

    def is_resolver(self):
        '''Return whether the service is a resolver service.'''
        return self.service_type == 'Resolver'
