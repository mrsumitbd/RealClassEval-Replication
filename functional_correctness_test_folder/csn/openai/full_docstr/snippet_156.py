
import xml.etree.ElementTree as ET
from typing import Dict


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

    def __init__(self, service_node: ET.Element):
        '''Initialize the Dataset object.
        Parameters
        ----------
        service_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a service node
        '''
        # Basic attributes
        self.name: str = service_node.attrib.get('name', '').strip()
        self.service_type: str = service_node.attrib.get('type', '').strip()

        # Collect access URLs
        self.access_urls: Dict[str, str] = {}
        # Common tag names for access URLs
        access_tag_names = ('accessURL', 'accessUrl', 'access_url')
        for tag in access_tag_names:
            for elem in service_node.findall(tag):
                # Determine the key (type) for the URL
                key = elem.attrib.get('type', '').strip()
                if not key:
                    # Fallback: use the tag name itself
                    key = tag
                # Determine the URL value
                url = elem.attrib.get('url')
                if url is None:
                    url = elem.text
                if url:
                    self.access_urls[key] = url.strip()

    def is_resolver(self) -> bool:
        '''Return whether the service is a resolver service.'''
        # Common resolver identifiers
        resolver_types = {'resolver', 'resolve', 'resolverservice'}
        if self.service_type.lower() in resolver_types:
            return True
        # Fallback: check if the name contains the word "resolver"
        return 'resolver' in self.name.lower()
