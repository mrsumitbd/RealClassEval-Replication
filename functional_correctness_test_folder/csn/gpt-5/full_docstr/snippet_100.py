import binascii
from ecdsa import VerifyingKey, SECP256k1


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self._dev = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        key_bytes = self._get_pubkey_bytes(identity, ecdh)
        return self._vk_from_bytes(key_bytes)

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        peer_bytes = self._ensure_compressed_pubkey(peer_pubkey)
        fn = (
            getattr(self._dev, "ecdh", None)
            or getattr(self._dev, "derive", None)
            or getattr(self._dev, "derive_ecdh", None)
            or getattr(self._dev, "ecdh_shared_secret", None)
        )
        if fn is None:
            raise AttributeError("Device does not support ECDH")
        secret = fn(identity, peer_bytes)
        if not isinstance(secret, (bytes, bytearray)):
            raise TypeError("Device ECDH must return bytes")
        return bytes(secret)

    # internal helpers

    def _get_pubkey_bytes(self, identity, ecdh):
        candidates = [
            ("pubkey", {"ecdh": ecdh}),
            ("pubkey", {}),
            ("get_pubkey", {"ecdh": ecdh}),
            ("get_pubkey", {}),
            ("get_public_key", {"ecdh": ecdh}),
            ("get_public_key", {}),
        ]
        for name, kwargs in candidates:
            fn = getattr(self._dev, name, None)
            if fn is None:
                continue
            try:
                res = fn(identity, **kwargs)
            except TypeError:
                # try positional ecdh if keyword not accepted
                try:
                    res = fn(identity, ecdh)
                except TypeError:
                    res = fn(identity)
            if not isinstance(res, (bytes, bytearray)):
                raise TypeError("Device pubkey method must return bytes")
            return bytes(res)
        raise AttributeError(
            "Device does not expose a pubkey retrieval method")

    def _vk_from_bytes(self, key_bytes):
        b = bytes(key_bytes)
        if len(b) == 33:
            return VerifyingKey.from_string(b, curve=SECP256k1, encoding="compressed")
        if len(b) == 65 and b[0] == 0x04:
            return VerifyingKey.from_string(b[1:], curve=SECP256k1, encoding="uncompressed")
        if len(b) == 64:
            return VerifyingKey.from_string(b, curve=SECP256k1, encoding="uncompressed")
        raise ValueError("Unsupported public key length/format")

    def _ensure_compressed_pubkey(self, peer_pubkey):
        # Accept VerifyingKey, bytes (compressed/uncompressed/raw), or hex string
        if isinstance(peer_pubkey, VerifyingKey):
            return peer_pubkey.to_string(encoding="compressed")
        if isinstance(peer_pubkey, str):
            s = peer_pubkey.strip().lower()
            if s.startswith("0x"):
                s = s[2:]
            b = binascii.unhexlify(s)
        elif isinstance(peer_pubkey, (bytes, bytearray)):
            b = bytes(peer_pubkey)
        else:
            raise TypeError(
                "peer_pubkey must be VerifyingKey, bytes or hex string")
        if len(b) == 33 and b[0] in (2, 3):
            return b
        if len(b) == 65 and b[0] == 0x04:
            # uncompressed with prefix, compress
            x = b[1:33]
            y = b[33:65]
            prefix = 0x02 | (y[-1] & 1)
            return bytes([prefix]) + x
        if len(b) == 64:
            # raw x||y, compress
            x = b[:32]
            y = b[32:]
            prefix = 0x02 | (y[-1] & 1)
            return bytes([prefix]) + x
        # If it's an unexpected length, try parsing as VerifyingKey via helper
        vk = self._vk_from_bytes(b)
        return vk.to_string(encoding="compressed")
