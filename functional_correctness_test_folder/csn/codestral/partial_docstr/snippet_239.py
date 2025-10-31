
from dataclasses import dataclass


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
    verify_cert: bytes
    verify_cert_ca: bytes = None
    encrypt_cert: bytes
    encrypt_cert_ca: bytes = None
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
        '''Run the post initialisation checks for this class.'''
        pass

    def load_verify_cert(self):
        '''Load the verification certificate of the partner and returned the parsed cert.'''
        pass

    def load_encrypt_cert(self):
        '''Load the encryption certificate of the partner and returned the parsed cert.'''
        pass
