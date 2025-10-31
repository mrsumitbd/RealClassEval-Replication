
import hashlib
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        # Ask the device for the raw public key bytes
        raw = self.device.get_pubkey(identity, ecdh=ecdh)

        # The device may return compressed (33 bytes) or uncompressed (65 bytes)
        if len(raw) == 33:
            # Compressed form: 0x02 or 0x03 prefix + 32-byte X coordinate
            try:
                vk = VerifyingKey.from_string(
                    raw, curve=SECP256k1, hashfunc=hashlib.sha256)
            except Exception:
                # Fallback: try to decompress manually
                vk = VerifyingKey.from_string(
                    raw, curve=SECP256k1, hashfunc=hashlib.sha256, validate_point=True)
        elif len(raw) == 65:
            # Uncompressed form: 0x04 prefix + X + Y
            # Strip the 0x04 prefix
            vk = VerifyingKey.from_string(
                raw[1:], curve=SECP256k1, hashfunc=hashlib.sha256)
        else:
            raise ValueError(f"Unexpected public key length: {len(raw)} bytes")

        return vk

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        # Convert the peer's VerifyingKey to the format expected by the device.
        # Most devices expect the compressed form.
        try:
            peer_bytes = peer_pubkey.to_string("compressed")
        except TypeError:
            # Fallback to uncompressed if compressed not supported
            peer_bytes = peer_pubkey.to_string()

        # Ask the device to perform ECDH with the peer's public key
        shared_secret = self.device.ecdh(
            identity, peer_pubkey_bytes=peer_bytes)

        return shared_secret
