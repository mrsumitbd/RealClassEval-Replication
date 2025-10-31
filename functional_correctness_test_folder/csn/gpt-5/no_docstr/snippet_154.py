class CatalogRef:

    def __init__(self, base_url, element_node):
        from urllib.parse import urljoin

        self.base_url = base_url
        self.element_node = element_node

        # Extract candidate URL from element_node
        href = None
        # If element_node is a string, treat it as the URL itself
        if isinstance(element_node, str):
            href = element_node.strip() or None
        else:
            # Try common element interfaces
            # lxml/ElementTree Elements support .get
            getter = getattr(element_node, "get", None)
            if callable(getter):
                href = getter("href") or getter("src") or getter("url")
            else:
                # Try .attrib dict
                attrib = getattr(element_node, "attrib", None)
                if isinstance(attrib, dict):
                    href = attrib.get("href") or attrib.get(
                        "src") or attrib.get("url")
                # Try mapping-like node
                if href is None and hasattr(element_node, "items"):
                    try:
                        mapping = dict(element_node.items())
                        href = mapping.get("href") or mapping.get(
                            "src") or mapping.get("url")
                    except Exception:
                        pass

        if href is None:
            # Fallback: try to use str(element_node) if it looks like a URL
            try:
                candidate = str(element_node).strip()
                if candidate:
                    href = candidate
            except Exception:
                href = None

        if href is None:
            raise ValueError("Cannot determine URL from element_node")

        self.url = urljoin(base_url or "", href)

    def __str__(self):
        return self.url

    def follow(self):
        import urllib.request
        import urllib.error

        if not self.url:
            raise ValueError("No URL to follow")

        req = urllib.request.Request(
            self.url,
            headers={
                "User-Agent": "CatalogRef/1.0 (+https://example.com)",
                "Accept": "*/*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            # Re-raise with original context; caller can handle
            raise
        except urllib.error.URLError as e:
            raise
