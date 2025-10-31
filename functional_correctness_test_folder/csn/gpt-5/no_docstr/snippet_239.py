from dataclasses import dataclass, field
from typing import Optional, Union
from pathlib import Path
import base64

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
except Exception as e:
    x509 = None
    default_backend = None


@dataclass
class Partner:
    verify_cert_source: Optional[Union[str, bytes, Path]] = None
    encrypt_cert_source: Optional[Union[str, bytes, Path]] = None

    verify_cert: Optional["x509.Certificate"] = field(
        default=None, init=False, repr=False)
    encrypt_cert: Optional["x509.Certificate"] = field(
        default=None, init=False, repr=False)

    def __post_init__(self):
        if x509 is None or default_backend is None:
            raise RuntimeError(
                "cryptography package is required to use Partner certificates")

        if self.verify_cert_source is not None:
            self.load_verify_cert()

        if self.encrypt_cert_source is not None:
            self.load_encrypt_cert()

    def _read_input_bytes(self, source: Union[str, bytes, Path]) -> bytes:
        if isinstance(source, bytes):
            return source
        if isinstance(source, Path):
            return source.read_bytes()
        # str
        s = source.strip()
        p = Path(s)
        if p.exists() and p.is_file():
            return p.read_bytes()
        return s.encode("utf-8")

    def _load_cert(self, source: Union[str, bytes, Path]) -> "x509.Certificate":
        data = self._read_input_bytes(source)

        # Try PEM first
        try:
            return x509.load_pem_x509_certificate(data, default_backend())
        except Exception:
            pass

        # If it's textual without PEM header, try to base64-decode into DER
        try:
            text = data.decode("utf-8", errors="ignore").strip()
            if "-----BEGIN" in text and "CERTIFICATE-----" in text:
                # It looked like PEM but failed earlier; raise a clear error
                raise ValueError("Invalid PEM certificate data")
            # Remove common header/footer if present in odd formatting
            cleaned = (
                text.replace("BEGIN CERTIFICATE", "")
                .replace("END CERTIFICATE", "")
                .replace("-----", "")
                .replace("\n", "")
                .replace("\r", "")
                .strip()
            )
            der = base64.b64decode(cleaned, validate=False)
            if der:
                try:
                    return x509.load_der_x509_certificate(der, default_backend())
                except Exception:
                    pass
        except Exception:
            pass

        # Try raw DER directly (if bytes provided)
        try:
            return x509.load_der_x509_certificate(data, default_backend())
        except Exception:
            pass

        raise ValueError(
            "Unable to load X.509 certificate from provided source")

    def load_verify_cert(self):
        if self.verify_cert_source is None:
            raise ValueError("verify_cert_source is not set")
        self.verify_cert = self._load_cert(self.verify_cert_source)
        return self.verify_cert

    def load_encrypt_cert(self):
        if self.encrypt_cert_source is None:
            raise ValueError("encrypt_cert_source is not set")
        self.encrypt_cert = self._load_cert(self.encrypt_cert_source)
        return self.encrypt_cert
