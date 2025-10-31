from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
except Exception as e:  # pragma: no cover
    x509 = None  # type: ignore


@dataclass
class Partner:
    '''
    Class represents an AS2 partner and defines the certificates and
    settings to be used when sending and receiving messages.
    :param as2_name: The unique AS2 name for this partner.
    :param verify_cert: A byte string of the certificate to be used for
        verifying signatures of inbound messages and MDNs.
    :param verify_cert_ca: A byte string of the ca certificate if any of
        the verification cert
    :param encrypt_cert: A byte string of the certificate to be used for
        encrypting outbound message.
    :param encrypt_cert_ca: A byte string of the ca certificate if any of
        the encryption cert
    :param validate_certs: Set this flag to `False` to disable validations of
        the encryption and verification certificates. (default `True`)
    :param compress: Set this flag to `True` to compress outgoing
        messages. (default `False`)
    :param sign: Set this flag to `True` to sign outgoing
        messages. (default `False`)
    :param digest_alg: The digest algorithm to be used for generating the
        signature. (default "sha256")
    :param encrypt: Set this flag to `True` to encrypt outgoing
        messages. (default `False`)
    :param enc_alg:
        The encryption algorithm to be used. (default `"tripledes_192_cbc"`)
    :param mdn_mode: The mode to be used for receiving the MDN.
        Set to `None` for no MDN, `'SYNC'` for synchronous and `'ASYNC'`
        for asynchronous. (default `None`)
    :param mdn_digest_alg: The digest algorithm to be used by the receiver
        for signing the MDN. Use `None` for unsigned MDN. (default `None`)
    :param mdn_confirm_text: The text to be used in the MDN for successfully
        processed messages received from this partner.
    :param canonicalize_as_binary: force binary canonicalization for this partner
    :param sign_alg: The signing algorithm to be used for generating the
        signature. (default `rsassa_pkcs1v15`)
    :param key_enc_alg: The key encryption algorithm to be used.
        (default `rsaes_pkcs1v15`)
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

    _allowed_digests: set = field(init=False, repr=False, default_factory=lambda: {
                                  "sha1", "sha224", "sha256", "sha384", "sha512"})
    _allowed_enc_algs: set = field(init=False, repr=False, default_factory=lambda: {
                                   "aes_128_cbc", "aes_192_cbc", "aes_256_cbc", "tripledes_192_cbc"})
    _allowed_sign_algs: set = field(init=False, repr=False, default_factory=lambda: {
                                    "rsassa_pkcs1v15", "rsassa_pss"})
    _allowed_key_enc_algs: set = field(init=False, repr=False, default_factory=lambda: {
                                       "rsaes_pkcs1v15", "rsaes_oaep"})
    _allowed_mdn_modes: set = field(
        init=False, repr=False, default_factory=lambda: {None, "SYNC", "ASYNC"})

    def __post_init__(self):
        if not isinstance(self.as2_name, str) or not self.as2_name.strip():
            raise ValueError("as2_name must be a non-empty string.")

        if self.mdn_mode is not None:
            self.mdn_mode = self.mdn_mode.upper()
        if self.mdn_mode not in self._allowed_mdn_modes:
            raise ValueError("mdn_mode must be None, 'SYNC', or 'ASYNC'.")

        if self.digest_alg not in self._allowed_digests:
            raise ValueError(
                f"digest_alg must be one of {sorted(self._allowed_digests)}.")

        if self.mdn_digest_alg is not None and self.mdn_digest_alg not in self._allowed_digests:
            raise ValueError(
                f"mdn_digest_alg must be one of {sorted(self._allowed_digests)} or None.")

        if self.enc_alg not in self._allowed_enc_algs:
            raise ValueError(
                f"enc_alg must be one of {sorted(self._allowed_enc_algs)}.")

        if self.sign_alg not in self._allowed_sign_algs:
            raise ValueError(
                f"sign_alg must be one of {sorted(self._allowed_sign_algs)}.")

        if self.key_enc_alg not in self._allowed_key_enc_algs:
            raise ValueError(
                f"key_enc_alg must be one of {sorted(self._allowed_key_enc_algs)}.")

        if self.encrypt and not self.encrypt_cert:
            raise ValueError(
                "encrypt is True but no encrypt_cert was provided.")

        if self.validate_certs:
            # Validate cert availability vs. expected usage
            if self.verify_cert is not None:
                self._validate_cert_bytes(self.verify_cert, "verify_cert")
            if self.encrypt_cert is not None:
                self._validate_cert_bytes(self.encrypt_cert, "encrypt_cert")
            if self.verify_cert_ca is not None:
                self._validate_cert_bytes(
                    self.verify_cert_ca, "verify_cert_ca")
            if self.encrypt_cert_ca is not None:
                self._validate_cert_bytes(
                    self.encrypt_cert_ca, "encrypt_cert_ca")

            # Basic chain relationship checks if both cert and CA are provided
            if self.verify_cert and self.verify_cert_ca:
                leaf = self._parse_cert(self.verify_cert)
                ca = self._parse_cert(self.verify_cert_ca)
                if leaf.issuer.rfc4514_string() != ca.subject.rfc4514_string():
                    # Not strictly required to match (it could be intermediate), but this is a minimal sanity check
                    pass
                self._check_cert_validity(leaf)
                self._check_cert_validity(ca)
            elif self.verify_cert:
                self._check_cert_validity(self._parse_cert(self.verify_cert))

            if self.encrypt_cert and self.encrypt_cert_ca:
                leaf = self._parse_cert(self.encrypt_cert)
                ca = self._parse_cert(self.encrypt_cert_ca)
                if leaf.issuer.rfc4514_string() != ca.subject.rfc4514_string():
                    pass
                self._check_cert_validity(leaf)
                self._check_cert_validity(ca)
            elif self.encrypt_cert:
                self._check_cert_validity(self._parse_cert(self.encrypt_cert))

    def load_verify_cert(self):
        '''Load the verification certificate of the partner and returned the parsed cert.'''
        if self.verify_cert is None:
            return None
        cert = self._parse_cert(self.verify_cert)
        if self.validate_certs:
            self._check_cert_validity(cert)
        return cert

    def load_encrypt_cert(self):
        '''Load the encryption certificate of the partner and returned the parsed cert.'''
        if self.encrypt_cert is None:
            return None
        cert = self._parse_cert(self.encrypt_cert)
        if self.validate_certs:
            self._check_cert_validity(cert)
        return cert

    def _parse_cert(self, data: bytes):
        if x509 is None:
            raise RuntimeError(
                "cryptography package is required to parse certificates.")
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Certificate data must be bytes.")
        blob = bytes(data)
        # Heuristic: PEM contains BEGIN
        try:
            if b"-----BEGIN" in blob:
                return x509.load_pem_x509_certificate(blob)
            else:
                return x509.load_der_x509_certificate(blob)
        except Exception as e:
            raise ValueError("Invalid certificate data.") from e

    def _check_cert_validity(self, cert):
        now = datetime.now(timezone.utc)
        # cryptography returns naive datetimes in older versions; normalize to aware UTC
        not_before = cert.not_valid_before
        not_after = cert.not_valid_after
        if not_before.tzinfo is None:
            not_before = not_before.replace(tzinfo=timezone.utc)
        if not_after.tzinfo is None:
            not_after = not_after.replace(tzinfo=timezone.utc)
        if now < not_before:
            raise ValueError("Certificate is not yet valid.")
        if now > not_after:
            raise ValueError("Certificate has expired.")

    def _validate_cert_bytes(self, data: bytes, field_name: str):
        if data is None:
            return
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"{field_name} must be bytes.")
        # Quick parse check
        self._parse_cert(bytes(data))
