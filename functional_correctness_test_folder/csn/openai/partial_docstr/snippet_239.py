
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from cryptography import x509
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate


@dataclass
class Partner:
    """
    Class represents an AS2 partner and defines the certificates and
    settings to be used when sending and receiving messages.
    """
    as2_name: str
    verify_cert: Optional[bytes] = None
    verify_cert_ca: Optional[bytes] = None
    encrypt_cert: Optional[bytes] = None
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

    def __post_init__(self) -> None:
        """Run the post initialisation checks for this class."""
        if not isinstance(self.as2_name, str) or not self.as2_name:
            raise ValueError("as2_name must be a non-empty string")

        # Validate certificate fields
        for name, cert in (
            ("verify_cert", self.verify_cert),
            ("verify_cert_ca", self.verify_cert_ca),
            ("encrypt_cert", self.encrypt_cert),
            ("encrypt_cert_ca", self.encrypt_cert_ca),
        ):
            if cert is not None and not isinstance(cert, (bytes, bytearray)):
                raise TypeError(f"{name} must be bytes or None")

        # If encryption is requested, an encryption cert must be supplied
        if self.encrypt and self.encrypt_cert is None:
            raise ValueError(
                "encrypt is True but encrypt_cert is not provided")

        # Validate mdn_mode
        if self.mdn_mode not in (None, "SYNC", "ASYNC"):
            raise ValueError("mdn_mode must be None, 'SYNC', or 'ASYNC'")

        # Validate mdn_digest_alg
        if self.mdn_digest_alg is not None and not isinstance(self.mdn_digest_alg, str):
            raise TypeError("mdn_digest_alg must be a string or None")

        # Validate digest algorithm (basic check)
        if not isinstance(self.digest_alg, str):
            raise TypeError("digest_alg must be a string")

        # Validate encryption algorithm
        if not isinstance(self.enc_alg, str):
            raise TypeError("enc_alg must be a string")

        # Validate sign algorithm
        if not isinstance(self.sign_alg, str):
            raise TypeError("sign_alg must be a string")

        # Validate key encryption algorithm
        if not isinstance(self.key_enc_alg, str):
            raise TypeError("key_enc_alg must be a string")

    def load_verify_cert(self) -> Optional[x509.Certificate]:
        """Load the verification certificate of the partner and return the parsed cert."""
        if self.verify_cert is None:
            return None
        try:
            cert = load_pem_x509_certificate(
                self.verify_cert, default_backend())
        except Exception as exc:
            raise ValueError("Failed to load verify_cert") from exc
        return cert

    def load_encrypt_cert(self) -> Optional[x509.Certificate]:
        """Load the encryption certificate of the partner and return the parsed cert."""
        if self.encrypt_cert is None:
            return None
        try:
            cert = load_pem_x509_certificate(
                self.encrypt_cert, default_backend())
        except Exception as exc:
            raise ValueError("Failed to load encrypt_cert") from exc
        return cert
