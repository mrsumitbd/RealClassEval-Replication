from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, List

from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, ed448, padding


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

    def __post_init__(self):
        if not isinstance(self.as2_name, str) or not self.as2_name.strip():
            raise ValueError("as2_name must be a non-empty string")

        if self.mdn_mode is not None:
            mode = self.mdn_mode.upper()
            if mode not in {"SYNC", "ASYNC"}:
                raise ValueError("mdn_mode must be None, 'SYNC' or 'ASYNC'")
            self.mdn_mode = mode

        allowed_digests = {"sha1", "sha256", "sha384", "sha512"}
        if self.digest_alg.lower() not in allowed_digests:
            raise ValueError(
                f"digest_alg must be one of {sorted(allowed_digests)}")

        if self.mdn_digest_alg is not None and self.mdn_digest_alg.lower() not in allowed_digests:
            raise ValueError(
                f"mdn_digest_alg must be one of {sorted(allowed_digests)} or None")

        allowed_enc_algs = {
            "tripledes_192_cbc",
            "aes128_cbc",
            "aes192_cbc",
            "aes256_cbc",
        }
        if self.enc_alg.lower() not in allowed_enc_algs:
            raise ValueError(
                f"enc_alg must be one of {sorted(allowed_enc_algs)}")

        allowed_sign_algs = {"rsassa_pkcs1v15", "rsassa_pss"}
        if self.sign_alg.lower() not in allowed_sign_algs:
            raise ValueError(
                f"sign_alg must be one of {sorted(allowed_sign_algs)}")

        allowed_key_enc_algs = {"rsaes_pkcs1v15", "rsaes_oaep"}
        if self.key_enc_alg.lower() not in allowed_key_enc_algs:
            raise ValueError(
                f"key_enc_alg must be one of {sorted(allowed_key_enc_algs)}")

        if self.encrypt and not self.encrypt_cert:
            raise ValueError("encrypt_cert must be provided when encrypt=True")

        if self.mdn_digest_alg is not None and not self.verify_cert:
            raise ValueError(
                "verify_cert must be provided when expecting signed MDNs (mdn_digest_alg set)")

        if self.validate_certs:
            if self.verify_cert:
                leaf = self._parse_single_cert(self.verify_cert)
                self._validate_cert_dates(leaf)
                cas = self._parse_cert_bundle(
                    self.verify_cert_ca) if self.verify_cert_ca else []
                if cas:
                    self._verify_issued_by_any(leaf, cas)
            if self.encrypt_cert:
                leaf = self._parse_single_cert(self.encrypt_cert)
                self._validate_cert_dates(leaf)
                cas = self._parse_cert_bundle(
                    self.encrypt_cert_ca) if self.encrypt_cert_ca else []
                if cas:
                    self._verify_issued_by_any(leaf, cas)

    def load_verify_cert(self) -> Optional[x509.Certificate]:
        if not self.verify_cert:
            return None
        cert = self._parse_single_cert(self.verify_cert)
        if self.validate_certs:
            self._validate_cert_dates(cert)
            if self.verify_cert_ca:
                cas = self._parse_cert_bundle(self.verify_cert_ca)
                if cas:
                    self._verify_issued_by_any(cert, cas)
        return cert

    def load_encrypt_cert(self) -> Optional[x509.Certificate]:
        if not self.encrypt_cert:
            return None
        cert = self._parse_single_cert(self.encrypt_cert)
        if self.validate_certs:
            self._validate_cert_dates(cert)
            if self.encrypt_cert_ca:
                cas = self._parse_cert_bundle(self.encrypt_cert_ca)
                if cas:
                    self._verify_issued_by_any(cert, cas)
        return cert

    def _parse_single_cert(self, data: bytes) -> x509.Certificate:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("certificate data must be bytes")
        try:
            return x509.load_pem_x509_certificate(data)
        except ValueError:
            try:
                return x509.load_der_x509_certificate(data)
            except ValueError as e:
                raise ValueError(
                    "Invalid certificate format, expected PEM or DER") from e

    def _parse_cert_bundle(self, data: Optional[bytes]) -> List[x509.Certificate]:
        if not data:
            return []
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("CA certificate data must be bytes")
        # Try PEM bundle first (multiple certs)
        certs: List[x509.Certificate] = []
        pem_marker = b"-----BEGIN CERTIFICATE-----"
        if pem_marker in data:
            chunks = data.split(pem_marker)
            for chunk in chunks:
                if not chunk.strip():
                    continue
                pem_block = pem_marker + \
                    chunk.split(
                        b"-----END CERTIFICATE-----")[0] + b"-----END CERTIFICATE-----\n"
                try:
                    certs.append(x509.load_pem_x509_certificate(pem_block))
                except Exception:
                    # Ignore blocks that fail to parse to allow mixed bundles
                    continue
        else:
            # Not PEM; attempt single DER
            try:
                certs.append(x509.load_der_x509_certificate(data))
            except Exception as e:
                raise ValueError("Invalid CA certificate data") from e
        return certs

    def _validate_cert_dates(self, cert: x509.Certificate) -> None:
        now = datetime.now(timezone.utc)
        # cryptography may return naive datetimes; interpret as UTC
        not_before = cert.not_valid_before
        not_after = cert.not_valid_after
        if not_before.tzinfo is None:
            not_before = not_before.replace(tzinfo=timezone.utc)
        if not_after.tzinfo is None:
            not_after = not_after.replace(tzinfo=timezone.utc)
        if now < not_before:
            raise ValueError("Certificate not yet valid")
        if now > not_after:
            raise ValueError("Certificate has expired")

    def _verify_issued_by_any(self, leaf: x509.Certificate, issuers: List[x509.Certificate]) -> None:
        last_error: Optional[Exception] = None
        for ca in issuers:
            try:
                self._verify_issued_by(leaf, ca)
                return
            except Exception as e:
                last_error = e
                continue
        if last_error:
            raise ValueError(
                "Certificate not issued by any provided CA") from last_error
        raise ValueError("No CA certificates provided for verification")

    def _verify_issued_by(self, leaf: x509.Certificate, ca: x509.Certificate) -> None:
        if leaf.issuer != ca.subject:
            raise ValueError("Issuer DN does not match CA subject")

        pub = ca.public_key()
        signature = leaf.signature
        data = leaf.tbs_certificate_bytes
        sig_hash = leaf.signature_hash_algorithm

        if isinstance(pub, rsa.RSAPublicKey):
            # Determine padding based on signature algorithm OID (assume PKCS1v15 for X.509)
            try:
                pub.verify(signature, data, padding.PKCS1v15(), sig_hash)
            except Exception as e:
                raise ValueError("RSA signature verification failed") from e
        elif isinstance(pub, ec.EllipticCurvePublicKey):
            try:
                pub.verify(signature, data, ec.ECDSA(sig_hash))
            except Exception as e:
                raise ValueError("ECDSA signature verification failed") from e
        elif isinstance(pub, ed25519.Ed25519PublicKey):
            try:
                pub.verify(signature, data)
            except Exception as e:
                raise ValueError(
                    "Ed25519 signature verification failed") from e
        elif isinstance(pub, ed448.Ed448PublicKey):
            try:
                pub.verify(signature, data)
            except Exception as e:
                raise ValueError("Ed448 signature verification failed") from e
        else:
            raise ValueError("Unsupported CA public key type for verification")

        # Optional: ensure CA has basicConstraints CA:TRUE if present
        try:
            bc = ca.extensions.get_extension_for_class(
                x509.BasicConstraints).value
            if not bc.ca:
                raise ValueError(
                    "Provided issuer certificate is not a CA certificate")
        except x509.ExtensionNotFound:
            # If extension not present, do not fail hard; many older CA certs may omit it
            pass

        # Extra: self-signed CA sanity check (not enforced)
        # Ensure leaf encodes to something; no-op to use Encoding (avoid lints)
        _ = leaf.public_bytes(Encoding.DER)
        _ = ca.public_bytes(Encoding.DER)
