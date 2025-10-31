from abc import ABC, abstractmethod

class Sse(ABC):
    """Server-side encryption base class."""

    @abstractmethod
    def headers(self) -> dict[str, str]:
        """Return headers."""

    def tls_required(self) -> bool:
        """Return TLS required to use this server-side encryption."""
        return True

    def copy_headers(self) -> dict[str, str]:
        """Return copy headers."""
        return {}