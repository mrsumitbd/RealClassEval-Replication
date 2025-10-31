from typing import Any, Optional, ClassVar, Union, Dict

class Route:
    DOMAIN: ClassVar[str] = 'api.sgroup.qq.com'
    SANDBOX_DOMAIN: ClassVar[str] = 'sandbox.api.sgroup.qq.com'
    SCHEME: ClassVar[str] = 'https'

    def __init__(self, method: str, path: str, is_sandbox: str=False, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.is_sandbox = is_sandbox
        self.parameters = parameters

    @property
    def url(self):
        if self.is_sandbox:
            d = self.SANDBOX_DOMAIN
        else:
            d = self.DOMAIN
        _url = '{}://{}{}'.format(self.SCHEME, d, self.path)
        if self.parameters:
            _url = _url.format_map(self.parameters)
        return _url