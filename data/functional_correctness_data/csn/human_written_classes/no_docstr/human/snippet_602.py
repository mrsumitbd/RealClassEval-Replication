from urllib.parse import urlparse

class _ResourceUri:

    def __init__(self, url: str):
        self.url = url
        self.parsed = urlparse(url)
        self.storage_account_name = self.parsed.netloc.split('.', 1)[0]
        self.object_name = self.parsed.path.lstrip('/')

    @property
    def account_uri(self) -> str:
        return f'{self.parsed.scheme}://{self.parsed.netloc}/?{self.parsed.query}'

    def __str__(self):
        return self.url