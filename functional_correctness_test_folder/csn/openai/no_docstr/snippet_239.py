
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Partner:
    """
    Represents a partner entity that holds certificates for verification and encryption.
    """
    # Paths to the certificate files
    verify_cert_path: Path | str
    encrypt_cert_path: Path | str

    # Loaded certificate data (bytes)
    verify_cert: Optional[bytes] = field(default=None, init=False)
    encrypt_cert: Optional[bytes] = field(default=None, init=False)

    def __post_init__(self):
        """
        Load certificates immediately after initialization.
        """
        self.load_verify_cert()
        self.load_encrypt_cert()

    def load_verify_cert(self):
        """
        Load the verification certificate from the specified path.
        """
        path = Path(self.verify_cert_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Verification certificate not found: {path}")
        with path.open("rb") as f:
            self.verify_cert = f.read()

    def load_encrypt_cert(self):
        """
        Load the encryption certificate from the specified path.
        """
        path = Path(self.encrypt_cert_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"Encryption certificate not found: {path}")
        with path.open("rb") as f:
            self.encrypt_cert = f.read()
