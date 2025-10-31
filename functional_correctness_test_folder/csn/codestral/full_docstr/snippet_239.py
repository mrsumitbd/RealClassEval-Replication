
from dataclasses import dataclass


@dataclass
class Partner:
    as2_name: str
    verify_cert: bytes
    verify_cert_ca: bytes
    encrypt_cert: bytes
    encrypt_cert_ca: bytes
    validate_certs: bool = True
    compress: bool = False
    sign: bool = False
    digest_alg: str = "sha256"
    encrypt: bool = False
    enc_alg: str = "tripledes_192_cbc"
    mdn_mode: str = None
    mdn_digest_alg: str = None
    mdn_confirm_text: str = None
    canonicalize_as_binary: bool = False
    sign_alg: str = "rsassa_pkcs1v15"
    key_enc_alg: str = "rsaes_pkcs1v15"

    def __post_init__(self):
        if not isinstance(self.as2_name, str):
            raise TypeError("as2_name must be a string")
        if not isinstance(self.verify_cert, bytes):
            raise TypeError("verify_cert must be a byte string")
        if not isinstance(self.verify_cert_ca, bytes):
            raise TypeError("verify_cert_ca must be a byte string")
        if not isinstance(self.encrypt_cert, bytes):
            raise TypeError("encrypt_cert must be a byte string")
        if not isinstance(self.encrypt_cert_ca, bytes):
            raise TypeError("encrypt_cert_ca must be a byte string")
        if not isinstance(self.validate_certs, bool):
            raise TypeError("validate_certs must be a boolean")
        if not isinstance(self.compress, bool):
            raise TypeError("compress must be a boolean")
        if not isinstance(self.sign, bool):
            raise TypeError("sign must be a boolean")
        if not isinstance(self.digest_alg, str):
            raise TypeError("digest_alg must be a string")
        if not isinstance(self.encrypt, bool):
            raise TypeError("encrypt must be a boolean")
        if not isinstance(self.enc_alg, str):
            raise TypeError("enc_alg must be a string")
        if self.mdn_mode is not None and not isinstance(self.mdn_mode, str):
            raise TypeError("mdn_mode must be a string or None")
        if self.mdn_digest_alg is not None and not isinstance(self.mdn_digest_alg, str):
            raise TypeError("mdn_digest_alg must be a string or None")
        if self.mdn_confirm_text is not None and not isinstance(self.mdn_confirm_text, str):
            raise TypeError("mdn_confirm_text must be a string or None")
        if not isinstance(self.canonicalize_as_binary, bool):
            raise TypeError("canonicalize_as_binary must be a boolean")
        if not isinstance(self.sign_alg, str):
            raise TypeError("sign_alg must be a string")
        if not isinstance(self.key_enc_alg, str):
            raise TypeError("key_enc_alg must be a string")

    def load_verify_cert(self):
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend

        cert = x509.load_pem_x509_certificate(
            self.verify_cert, default_backend())
        return cert

    def load_encrypt_cert(self):
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend

        cert = x509.load_pem_x509_certificate(
            self.encrypt_cert, default_backend())
        return cert
