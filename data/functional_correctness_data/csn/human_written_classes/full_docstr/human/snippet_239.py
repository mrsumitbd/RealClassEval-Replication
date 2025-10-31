from oscrypto import asymmetric
from pyas2lib.exceptions import AS2Exception, DuplicateDocument, ImproperlyConfigured, InsufficientSecurityError, IntegrityError, MDNNotFound, PartnerNotFound
from pyas2lib.utils import canonicalize, extract_first_part, make_mime_boundary, mime_to_bytes, pem_to_der, quote_as2name, split_pem, unquote_as2name, verify_certificate_chain
from pyas2lib.constants import AS2_VERSION, ASYNCHRONOUS_MDN, DIGEST_ALGORITHMS, EDIINT_FEATURES, ENCRYPTION_ALGORITHMS, KEY_ENCRYPTION_ALGORITHMS, MDN_CONFIRM_TEXT, MDN_FAILED_TEXT, MDN_MODES, SIGNATUR_ALGORITHMS, SYNCHRONOUS_MDN
from dataclasses import dataclass

@dataclass
class Partner:
    """
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

    """
    as2_name: str
    verify_cert: bytes = None
    verify_cert_ca: bytes = None
    encrypt_cert: bytes = None
    encrypt_cert_ca: bytes = None
    validate_certs: bool = True
    compress: bool = False
    encrypt: bool = False
    enc_alg: str = 'tripledes_192_cbc'
    sign: bool = False
    digest_alg: str = 'sha256'
    mdn_mode: str = None
    mdn_digest_alg: str = None
    mdn_confirm_text: str = MDN_CONFIRM_TEXT
    ignore_self_signed: bool = True
    canonicalize_as_binary: bool = False
    sign_alg: str = 'rsassa_pkcs1v15'
    key_enc_alg: str = 'rsaes_pkcs1v15'

    def __post_init__(self):
        """Run the post initialisation checks for this class."""
        if self.digest_alg and self.digest_alg not in DIGEST_ALGORITHMS:
            raise ImproperlyConfigured(f'Unsupported Digest Algorithm {self.digest_alg}, must be one of {DIGEST_ALGORITHMS}')
        if self.enc_alg and self.enc_alg not in ENCRYPTION_ALGORITHMS:
            raise ImproperlyConfigured(f'Unsupported Encryption Algorithm {self.enc_alg}, must be one of {ENCRYPTION_ALGORITHMS}')
        if self.mdn_mode and self.mdn_mode not in MDN_MODES:
            raise ImproperlyConfigured(f'Unsupported MDN Mode {self.mdn_mode}, must be one of {MDN_MODES}')
        if self.mdn_digest_alg and self.mdn_digest_alg not in DIGEST_ALGORITHMS:
            raise ImproperlyConfigured(f'Unsupported MDN Digest Algorithm {self.mdn_digest_alg}, must be one of {DIGEST_ALGORITHMS}')
        if self.sign_alg and self.sign_alg not in SIGNATUR_ALGORITHMS:
            raise ImproperlyConfigured(f'Unsupported Signature Algorithm {self.sign_alg}, must be one of {SIGNATUR_ALGORITHMS}')
        if self.key_enc_alg and self.key_enc_alg not in KEY_ENCRYPTION_ALGORITHMS:
            raise ImproperlyConfigured(f'Unsupported Key Encryption Algorithm {self.key_enc_alg}, must be one of {KEY_ENCRYPTION_ALGORITHMS}')

    def load_verify_cert(self):
        """Load the verification certificate of the partner and returned the parsed cert."""
        if self.validate_certs:
            cert = pem_to_der(self.verify_cert, return_multiple=False)
            if self.verify_cert_ca:
                trust_roots = pem_to_der(self.verify_cert_ca)
            else:
                trust_roots = []
            verify_certificate_chain(cert, trust_roots, ignore_self_signed=self.ignore_self_signed)
        return asymmetric.load_certificate(self.verify_cert)

    def load_encrypt_cert(self):
        """Load the encryption certificate of the partner and returned the parsed cert."""
        if self.validate_certs:
            cert = pem_to_der(self.encrypt_cert, return_multiple=False)
            if self.encrypt_cert_ca:
                trust_roots = pem_to_der(self.encrypt_cert_ca)
            else:
                trust_roots = []
            verify_certificate_chain(cert, trust_roots, ignore_self_signed=self.ignore_self_signed)
        return asymmetric.load_certificate(self.encrypt_cert)