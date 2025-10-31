
from dataclasses import dataclass, field
from typing import Optional
import ssl


@dataclass
class Partner:
    verify_cert_path: str = field(default_factory=str)
    encrypt_cert_path: str = field(default_factory=str)
    verify_cert: Optional[ssl.SSLContext] = field(init=False, default=None)
    encrypt_cert: Optional[ssl.SSLContext] = field(init=False, default=None)

    def __post_init__(self):
        self.load_verify_cert()
        self.load_encrypt_cert()

    def load_verify_cert(self):
        if self.verify_cert_path:
            self.verify_cert = ssl.create_default_context(
                cafile=self.verify_cert_path)

    def load_encrypt_cert(self):
        if self.encrypt_cert_path:
            self.encrypt_cert = ssl.create_default_context()
            self.encrypt_cert.load_cert_chain(certfile=self.encrypt_cert_path)
