
from dataclasses import dataclass, field
from typing import Optional
import ssl
import tempfile


@dataclass
class Partner:
    '''
    Class represents an AS2 partner and defines the certificates and
    settings to be used when sending and receiving messages.
    '''
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

    def __post_init__(self):
        if not isinstance(self.as2_name, str) or not self.as2_name:
            raise ValueError("as2_name must be a non-empty string")
        if self.mdn_mode not in (None, 'SYNC', 'ASYNC'):
            raise ValueError("mdn_mode must be None, 'SYNC', or 'ASYNC'")
        if self.digest_alg is not None and not isinstance(self.digest_alg, str):
            raise ValueError("digest_alg must be a string or None")
        if self.mdn_digest_alg is not None and not isinstance(self.mdn_digest_alg, str):
            raise ValueError("mdn_digest_alg must be a string or None")
        if self.enc_alg is not None and not isinstance(self.enc_alg, str):
            raise ValueError("enc_alg must be a string or None")
        if self.sign_alg is not None and not isinstance(self.sign_alg, str):
            raise ValueError("sign_alg must be a string or None")
        if self.key_enc_alg is not None and not isinstance(self.key_enc_alg, str):
            raise ValueError("key_enc_alg must be a string or None")
        if self.verify_cert is not None and not isinstance(self.verify_cert, bytes):
            raise ValueError("verify_cert must be bytes or None")
        if self.verify_cert_ca is not None and not isinstance(self.verify_cert_ca, bytes):
            raise ValueError("verify_cert_ca must be bytes or None")
        if self.encrypt_cert is not None and not isinstance(self.encrypt_cert, bytes):
            raise ValueError("encrypt_cert must be bytes or None")
        if self.encrypt_cert_ca is not None and not isinstance(self.encrypt_cert_ca, bytes):
            raise ValueError("encrypt_cert_ca must be bytes or None")

    def load_verify_cert(self):
        '''Load the verification certificate of the partner and returned the parsed cert.'''
        if self.verify_cert is None:
            raise ValueError("No verify_cert provided")
        return self._load_cert(self.verify_cert, self.verify_cert_ca)

    def load_encrypt_cert(self):
        '''Load the encryption certificate of the partner and returned the parsed cert.'''
        if self.encrypt_cert is None:
            raise ValueError("No encrypt_cert provided")
        return self._load_cert(self.encrypt_cert, self.encrypt_cert_ca)

    def _load_cert(self, cert_bytes, ca_bytes):
        # This function returns an ssl.SSLContext with the cert loaded for demonstration.
        # In real AS2, you might use cryptography.x509 for more advanced parsing.
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(cert_bytes)
            cert_file.flush()
            if ca_bytes:
                with tempfile.NamedTemporaryFile(delete=False) as ca_file:
                    ca_file.write(ca_bytes)
                    ca_file.flush()
                    context.load_verify_locations(cafile=ca_file.name)
            else:
                context.load_verify_locations(cafile=cert_file.name)
        return context
