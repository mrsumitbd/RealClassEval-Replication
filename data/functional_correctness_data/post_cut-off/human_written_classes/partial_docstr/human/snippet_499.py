import time
from typing import Any

class JwtPayload:
    """
    Represents the payload (claims) of a JSON Web Token for APIM testing.
    https://datatracker.ietf.org/doc/html/rfc7519
    """
    DEFAULT_LIFETIME_SECONDS = 3600 * 24

    def __init__(self, subject: str, name: str, issued_at: int | None=None, expires: int | None=None, roles: dict[str] | None=None) -> None:
        self.sub = subject
        self.name = name
        self.iat = issued_at if issued_at is not None else int(time.time())
        self.exp = expires if expires is not None else self.iat + self.DEFAULT_LIFETIME_SECONDS
        self.roles = roles if roles is not None else []

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the payload to a dictionary for encoding.
        """
        pl: dict[str, Any] = {'sub': self.sub, 'name': self.name, 'iat': self.iat, 'exp': self.exp}
        if bool(self.roles):
            pl['roles'] = self.roles
        return pl