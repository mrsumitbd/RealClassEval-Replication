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
        self.name = None
        self.service_type = None
        self.access_urls = {}

        # Support mapping-like inputs
        try:
            from collections.abc import Mapping
            is_mapping = isinstance(service_node, Mapping)
        except Exception:
            is_mapping = False

        # Support xml.etree.ElementTree Element inputs
        try:
            from xml.etree.ElementTree import Element
            is_xml_element = isinstance(service_node, Element)
        except Exception:
            is_xml_element = False

        if is_mapping:
            self._init_from_mapping(service_node)
        elif is_xml_element:
            self._init_from_xml(service_node)
        else:
            # Fallback: attempt to coerce basic tuple/list or object with attributes
            self._init_from_generic(service_node)

        # Normalize keys of access_urls to strings and strip whitespace
        self.access_urls = {
            (str(k).strip() if k is not None else ''): (v.strip() if isinstance(v, str) else v)
            for k, v in self.access_urls.items()
            if k is not None and v is not None
        }

        # Normalize name and service_type
        if isinstance(self.name, str):
            self.name = self.name.strip()
        if isinstance(self.service_type, str):
            self.service_type = self.service_type.strip()

    def _init_from_mapping(self, m):
        # Direct fields
        self.name = m.get('name') or m.get(
            'Name') or m.get('id') or m.get('ID')
        self.service_type = (
            m.get('service_type')
            or m.get('serviceType')
            or m.get('type')
            or m.get('Type')
        )
        # Access URLs directly provided
        access = (
            m.get('access_urls')
            or m.get('accessUrls')
            or m.get('access')
            or m.get('urls')
        )
        if isinstance(access, dict):
            self.access_urls.update(access)
        elif isinstance(access, (list, tuple)):
            # if list of (type, url) pairs
            for item in access:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    key, val = item[0], item[1]
                    if key is not None and val is not None:
                        self.access_urls[str(key)] = str(val)
        # Look for flat keys like 'OPENDAP', 'WMS', etc.
        for k, v in m.items():
            if k and isinstance(k, str) and v and isinstance(v, str):
                upper_k = k.upper()
                if upper_k in ('OPENDAP', 'DAP', 'WMS', 'WCS', 'HTTPServer', 'HTTP', 'NetcdfSubset', 'NCSS', 'CDMRemote', 'Resolver', 'RESOLVER'):
                    self.access_urls[upper_k] = v

        # Sometimes nested children describing services
        children = m.get('children') or m.get('services') or []
        if isinstance(children, dict):
            children = [children]
        if isinstance(children, (list, tuple)):
            for child in children:
                if isinstance(child, dict):
                    st = child.get('serviceType') or child.get(
                        'type') or child.get('service_type')
                    url = child.get('url') or child.get(
                        'urlPath') or child.get('href') or child.get('link')
                    if st and url:
                        self.access_urls[str(st)] = str(url)

    def _init_from_xml(self, elem):
        # Attributes on the element
        self.name = elem.attrib.get('name') or elem.attrib.get(
            'id') or elem.attrib.get('ID')
        self.service_type = elem.attrib.get(
            'serviceType') or elem.attrib.get('type')

        # Direct URL attributes
        direct_url = elem.attrib.get('url') or elem.attrib.get('href')
        if direct_url and self.service_type:
            self.access_urls[self.service_type] = direct_url

        # Handle THREDDS-like "access" child elements or nested services
        for child in list(elem):
            tag = child.tag.split('}')[-1]  # strip namespace if present
            if tag.lower() in ('access', 'service'):
                st = child.attrib.get(
                    'serviceType') or child.attrib.get('type')
                url = child.attrib.get('url') or child.attrib.get(
                    'urlPath') or child.attrib.get('href')
                if st and url:
                    self.access_urls[st] = url

            # Generic pattern: any child with serviceType and url/href/urlPath
            st = child.attrib.get('serviceType') or child.attrib.get('type')
            if st:
                url = child.attrib.get('url') or child.attrib.get(
                    'href') or child.attrib.get('urlPath')
                if url:
                    self.access_urls[st] = url

    def _init_from_generic(self, obj):
        # Try attribute access
        self.name = getattr(obj, 'name', None) or getattr(obj, 'id', None)
        self.service_type = getattr(obj, 'service_type', None) or getattr(
            obj, 'serviceType', None) or getattr(obj, 'type', None)

        access = getattr(obj, 'access_urls', None) or getattr(
            obj, 'access', None) or getattr(obj, 'urls', None)
        if isinstance(access, dict):
            self.access_urls.update(access)
        elif isinstance(access, (list, tuple)):
            for item in access:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    k, v = item[0], item[1]
                    if k is not None and v is not None:
                        self.access_urls[str(k)] = str(v)

        # If object has iterable children
        children = getattr(obj, 'children', None) or getattr(
            obj, 'services', None)
        if isinstance(children, (list, tuple)):
            for child in children:
                st = getattr(child, 'service_type', None) or getattr(
                    child, 'serviceType', None) or getattr(child, 'type', None)
                url = getattr(child, 'url', None) or getattr(
                    child, 'href', None) or getattr(child, 'urlPath', None)
                if st and url:
                    self.access_urls[str(st)] = str(url)

    def is_resolver(self):
        '''Return whether the service is a resolver service.'''
        if not self.service_type:
            return False
        return str(self.service_type).strip().lower() == 'resolver'
