import hashlib
from aredis.utils import b

class IdentityGenerator:
    """
    Generator of identity for unique key,
    you may overwrite it to meet your customize requirements.
    """
    TEMPLATE = '{app}:{key}:{content}'

    def __init__(self, app, encoding='utf-8'):
        self.app = app
        self.encoding = encoding

    def _trans_type(self, content):
        if isinstance(content, str):
            content = content.encode(self.encoding)
        elif isinstance(content, int):
            content = b(str(content))
        elif isinstance(content, float):
            content = b(repr(content))
        return content

    def generate(self, key, content):
        content = self._trans_type(content)
        md5 = hashlib.md5()
        md5.update(content)
        hash = md5.hexdigest()
        identity = self.TEMPLATE.format(app=self.app, key=key, content=hash)
        return identity