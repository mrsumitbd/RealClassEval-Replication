
from dataclasses import dataclass, field


@dataclass
class Partner:
    verify_cert_path: str = field(default="")
    encrypt_cert_path: str = field(default="")
    verify_cert: bytes = field(init=False, default=None)
    encrypt_cert: bytes = field(init=False, default=None)

    def __post_init__(self):
        if self.verify_cert_path:
            self.load_verify_cert()
        if self.encrypt_cert_path:
            self.load_encrypt_cert()

    def load_verify_cert(self):
        with open(self.verify_cert_path, "rb") as f:
            self.verify_cert = f.read()

    def load_encrypt_cert(self):
        with open(self.encrypt_cert_path, "rb") as f:
            self.encrypt_cert = f.read()
