
class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node
        self.href = element_node.get('xlink:href') or element_node.get('href')

    def __str__(self):
        return f"CatalogRef(href={self.href})"

    def follow(self):
        import urllib.parse
        if self.href is None:
            return None
        return urllib.parse.urljoin(self.base_url, self.href)
