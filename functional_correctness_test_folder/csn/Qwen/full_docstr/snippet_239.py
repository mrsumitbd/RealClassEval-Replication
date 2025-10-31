
from dataclasses import dataclass, field
from typing import Optional, Union
from cryptography import x509
from cryptography.hazmat.backends import default_backend


@dataclass
class Partner:
    as2_name: str
    verify_cert: bytes
    verify_cert_ca: Optional[bytes] = None
    encrypt_cert: bytes
    encrypt_cert_ca: Optional[bytes] = None
    validate_certs: bool = True
    compress: bool = False
    sign: bool = False
    digest_alg: str = "sha256"
    encrypt: bool = False
    enc_alg: str = "tripledes_192_cbc"
    mdn_mode: Optional[str] = None
    mdn_digest_alg: Optional[str] = None
    mdn_confirm_text: Optional[str] = None
    canonicalize_as_binary: bool = False
    sign_alg: str = "rsassa_pkcs1v15"
    key_enc_alg: str = "rsaes_pkcs1v15"

    def __post_init__(self):
        if self.validate_certs:
            self.load_verify_cert()
            self.load_encrypt_cert()

    def load_verify_cert(self) -> x509.Certificate:
        return x509.load_pem_x509_certificate(self.verify_cert, default_backend())

    def load_encrypt_cert(self) -> x509.Certificate:
        return x509.load_pem_x509_certificate(self.encrypt_cert, default_backend())
