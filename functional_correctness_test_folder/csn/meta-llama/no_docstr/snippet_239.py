
from dataclasses import dataclass
import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend


@dataclass
class Partner:
    name: str
    verify_cert_path: str
    encrypt_cert_path: str
    verify_cert: x509.Certificate = None
    encrypt_cert: x509.Certificate = None

    def __post_init__(self):
        self.load_verify_cert()
        self.load_encrypt_cert()

    def load_verify_cert(self):
        if not os.path.exists(self.verify_cert_path):
            raise FileNotFoundError(
                f"Verify certificate file not found: {self.verify_cert_path}")

        with open(self.verify_cert_path, 'rb') as f:
            self.verify_cert = x509.load_pem_x509_certificate(
                f.read(), default_backend())

    def load_encrypt_cert(self):
        if not os.path.exists(self.encrypt_cert_path):
            raise FileNotFoundError(
                f"Encrypt certificate file not found: {self.encrypt_cert_path}")

        with open(self.encrypt_cert_path, 'rb') as f:
            self.encrypt_cert = x509.load_pem_x509_certificate(
                f.read(), default_backend())
