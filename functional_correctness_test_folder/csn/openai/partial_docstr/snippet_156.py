
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
        # service_node may be an lxml Element or a plain dict
        if isinstance(service_node, dict):
            self.name = service_node.get('name')
            self.service_type = service_node.get('service_type')
            access = service_node.get('access_urls', {})
            # ensure dict of str->str
            self.access_urls = {k: str(v) for k, v in access.items()}
        else:
            # assume Element
            self.name = service_node.get('name')
            if self.name is None:
                self.name = service_node.findtext('name')
            self.service_type = service_node.get('service_type')
            if self.service_type is None:
                self.service_type = service_node.findtext('service_type')
            self.access_urls = {}
            for child in service_node.findall('.//access_url'):
                # try attributes first
                typ = child.get('type')
                url = child.get('url')
                # fallback to subelements
                if typ is None:
                    typ = child.findtext('type')
                if url is None:
                    url = child.findtext('url')
                if typ and url:
                    self.access_urls[typ] = url

    def is_resolver(self):
        '''Return whether the service is a resolver service.'''
        if self.service_type:
            return self.service_type.lower() == 'resolver'
        if self.name:
            return 'resolver' in self.name.lower()
        return False
