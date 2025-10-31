
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from cryptography import x509
from cryptography.hazmat.backends import default_backend


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
    mdn_mode: Optional[str] = None  # None, 'SYNC', 'ASYNC'
    mdn_digest_alg: Optional[str] = None
    mdn_confirm_text: Optional[str] = None
    canonicalize_as_binary: bool = False
    sign_alg: str = "rsassa_pkcs1v15"
    key_enc_alg: str = "rsaes_pkcs1v15"

    # Parsed certificates (cached after loading)
    _verify_cert_obj: Optional[x509.Certificate] = field(
        default=None, init=False, repr=False)
    _encrypt_cert_obj: Optional[x509.Certificate] = field(
        default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Run the post initialisation checks for this class."""
        # Basic validation of required certificates
        if self.verify_cert is None:
            raise ValueError("verify_cert must be provided")
        if self.encrypt_cert is None:
            raise ValueError("encrypt_cert must be provided")

        # Validate mdn_mode
        if self.mdn_mode not in (None, "SYNC", "ASYNC"):
            raise ValueError("mdn_mode must be None, 'SYNC', or 'ASYNC'")

        # Validate digest algorithm (basic check)
        if not isinstance(self.digest_alg, str) or not self.digest_alg:
            raise ValueError("digest_alg must be a non-empty string")

        # Validate encryption algorithm (basic check)
        if not isinstance(self.enc_alg, str) or not self.enc_alg:
            raise ValueError("enc_alg must be a non-empty string")

        # Validate sign algorithm
        if not isinstance(self.sign_alg, str) or not self.sign_alg:
            raise ValueError("sign_alg must be a non-empty string")

        # Validate key encryption algorithm
        if not isinstance(self.key_enc_alg, str) or not self.key_enc_alg:
            raise ValueError("key_enc_alg must be a non-empty string")

        # If validation is disabled, skip certificate checks
        if not self.validate_certs:
            return

        # Load certificates to ensure they are valid PEM
        self._verify_cert_obj = self.load_verify_cert()
        self._encrypt_cert_obj = self.load_encrypt_cert()

        # Optionally load CA certificates if provided
        if self.verify_cert_ca:
            try:
                x509.load_pem_x509_certificate(
                    self.verify_cert_ca, default_backend())
            except Exception as exc:
                raise ValueError(
                    "verify_cert_ca is not a valid PEM certificate") from exc
        if self.encrypt_cert_ca:
            try:
                x509.load_pem_x509_certificate(
                    self.encrypt_cert_ca, default_backend())
            except Exception as exc:
                raise ValueError(
                    "encrypt_cert_ca is not a valid PEM certificate") from exc

    def load_verify_cert(self) -> x509.Certificate:
        """Load the verification certificate of the partner and return the parsed cert."""
        if self.verify_cert is None:
            raise ValueError("verify_cert is not set")
        try:
            cert = x509.load_pem_x509_certificate(
                self.verify_cert, default_backend())
        except Exception as exc:
            raise ValueError(
                "verify_cert is not a valid PEM certificate") from exc
        return cert

    def load_encrypt_cert(self) -> x509.Certificate:
        """Load the encryption certificate of the partner and return the parsed cert."""
        if self.encrypt_cert is None:
            raise ValueError("encrypt_cert is not set")
        try:
            cert = x509.load_pem_x509_certificate(
                self.encrypt_cert, default_backend())
        except Exception as exc:
            raise ValueError(
                "encrypt_cert is not a valid PEM certificate") from exc
        return cert
