import json

class HTTPResponseWrapper:

    def __init__(self, content: bytes, status_code: int):
        self.content = content
        self.status_code = status_code

    def json(self):
        return json.loads(self.content)

    @property
    def text(self) -> str:
        return self.content.decode('utf-8')

    def getcode(self) -> int:
        return self.status_code