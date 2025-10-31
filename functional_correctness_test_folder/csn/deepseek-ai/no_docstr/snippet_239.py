
from dataclasses import dataclass
from typing import Optional


@dataclass
class Partner:
    verify_cert: Optional[str] = None
    encrypt_cert: Optional[str] = None

    def __post_init__(self):
        if self.verify_cert is not None:
            self.load_verify_cert()
        if self.encrypt_cert is not None:
            self.load_encrypt_cert()

    def load_verify_cert(self):
        # Implement certificate loading logic here
        pass

    def load_encrypt_cert(self):
        # Implement certificate loading logic here
        pass
