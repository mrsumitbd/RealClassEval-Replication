from pyas2lib.constants import AS2_VERSION, ASYNCHRONOUS_MDN, DIGEST_ALGORITHMS, EDIINT_FEATURES, ENCRYPTION_ALGORITHMS, KEY_ENCRYPTION_ALGORITHMS, MDN_CONFIRM_TEXT, MDN_FAILED_TEXT, MDN_MODES, SIGNATUR_ALGORITHMS, SYNCHRONOUS_MDN
from pyas2lib.utils import canonicalize, extract_first_part, make_mime_boundary, mime_to_bytes, pem_to_der, quote_as2name, split_pem, unquote_as2name, verify_certificate_chain
from pyas2lib.exceptions import AS2Exception, DuplicateDocument, ImproperlyConfigured, InsufficientSecurityError, IntegrityError, MDNNotFound, PartnerNotFound
from oscrypto import asymmetric
from dataclasses import dataclass

@dataclass
class Organization:
    """
    Class represents an AS2 organization and defines the certificates and
    settings to be used when sending and receiving messages.

    :param as2_name: The unique AS2 name for this organization

    :param sign_key: A byte string of the pkcs12 encoded key pair
        used for signing outbound messages and MDNs.

    :param sign_key_pass: The password for decrypting the `sign_key`

    :param decrypt_key:  A byte string of the pkcs12 encoded key pair
        used for decrypting inbound messages.

    :param decrypt_key_pass: The password for decrypting the `decrypt_key`

    :param mdn_url: The URL where the receiver is expected to post
        asynchronous MDNs.

    :param domain:
        Optional domain if given provides the portion of the message id
        after the '@'.  It defaults to the locally defined hostname.
    """
    as2_name: str
    sign_key: bytes = None
    sign_key_pass: str = None
    decrypt_key: bytes = None
    decrypt_key_pass: str = None
    mdn_url: str = None
    mdn_confirm_text: str = MDN_CONFIRM_TEXT
    domain: str = None

    def __post_init__(self):
        """Run the post initialisation checks for this class."""
        if self.sign_key:
            self.sign_key = self.load_key(self.sign_key, self.sign_key_pass)
        if self.decrypt_key:
            self.decrypt_key = self.load_key(self.decrypt_key, self.decrypt_key_pass)

    @staticmethod
    def load_key(key_str: bytes, key_pass: str):
        """Function to load password protected key file in p12 or pem format."""
        try:
            key, cert, _ = asymmetric.load_pkcs12(key_str, key_pass)
        except ValueError as e:
            if e.args[0] == 'Password provided is invalid':
                raise AS2Exception('Password not valid for Private Key.') from e
            key, cert = (None, None)
            for kc in split_pem(key_str):
                try:
                    cert = asymmetric.load_certificate(kc)
                except (ValueError, TypeError) as e:
                    try:
                        key = asymmetric.load_private_key(kc, key_pass)
                    except OSError:
                        raise AS2Exception('Invalid Private Key or password is not correct.') from e
        if not key or not cert:
            raise AS2Exception('Invalid Private key file or Public key not included.')
        return (key, cert)