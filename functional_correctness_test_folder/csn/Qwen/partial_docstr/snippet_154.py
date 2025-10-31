
import xml.etree.ElementTree as ET
import requests


class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node
        self.href = element_node.get('href')
        self.catalog_url = self._construct_catalog_url()

    def __str__(self):
        return f"CatalogRef(base_url={self.base_url}, href={self.href})"

    def follow(self):
        response = requests.get(self.catalog_url)
        if response.status_code == 200:
            return ET.fromstring(response.content)
        else:
            raise Exception(
                f"Failed to fetch catalog at {self.catalog_url}, status code: {response.status_code}")

    def _construct_catalog_url(self):
        if self.href.startswith('http'):
            return self.href
        else:
            return f"{self.base_url.rstrip('/')}/{self.href.lstrip('/')}"
