import ecdsa


class Client:

    def __init__(self, device):
        '''C-tor.'''
        self.device = device
        self.curve = ecdsa.NIST256p

    def _get_sk(self, identity, ecdh=False):
        keyspace = 'ecdh' if ecdh else 'sign'
        sk = None
        stored = None

        # Try dict-like storage with composite key
        if hasattr(self.device, 'get'):
            try:
                stored = self.device.get((keyspace, identity))
            except TypeError:
                stored = None

        if isinstance(stored, ecdsa.SigningKey):
            sk = stored
        elif isinstance(stored, (bytes, bytearray)):
            sk = ecdsa.SigningKey.from_string(bytes(stored), curve=self.curve)

        # Try device methods
        if sk is None:
            for name in ('get_key', 'get_sk', 'get_signing_key'):
                if hasattr(self.device, name):
                    meth = getattr(self.device, name)
                    try:
                        maybe = meth(identity, ecdh=ecdh)
                    except TypeError:
                        try:
                            maybe = meth(identity)
                        except Exception:
                            continue
                    if isinstance(maybe, ecdsa.SigningKey):
                        sk = maybe
                        break
                    if isinstance(maybe, (bytes, bytearray)):
                        sk = ecdsa.SigningKey.from_string(
                            bytes(maybe), curve=self.curve)
                        break

        # Generate and store if still missing
        if sk is None:
            sk = ecdsa.SigningKey.generate(curve=self.curve)
            # Try dict-like storage
            try:
                if hasattr(self.device, '__setitem__'):
                    self.device[(keyspace, identity)] = sk.to_string()
            except Exception:
                pass
            # Try device setter methods
            for name in ('set_key', 'store_key', 'put_key'):
                if hasattr(self.device, name):
                    setter = getattr(self.device, name)
                    try:
                        setter(identity, sk.to_string(), ecdh=ecdh)
                        break
                    except TypeError:
                        try:
                            setter(identity, sk.to_string())
                            break
                        except Exception:
                            continue

        return sk

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        sk = self._get_sk(identity, ecdh=ecdh)
        return sk.get_verifying_key()

    def ecdh(self, identity, peer_pubkey):
        sk = self._get_sk(identity, ecdh=True)

        # Normalize peer_pubkey to VerifyingKey
        if isinstance(peer_pubkey, ecdsa.VerifyingKey):
            vk = peer_pubkey
        elif isinstance(peer_pubkey, (bytes, bytearray)):
            try:
                vk = ecdsa.VerifyingKey.from_string(
                    bytes(peer_pubkey), curve=self.curve)
            except Exception:
                # Attempt hex-decoding if it failed
                s = bytes(peer_pubkey).decode()
                vk = ecdsa.VerifyingKey.from_string(
                    bytes.fromhex(s), curve=self.curve)
        elif isinstance(peer_pubkey, str):
            s = peer_pubkey.strip()
            if "BEGIN PUBLIC KEY" in s or "BEGIN EC PUBLIC KEY" in s:
                vk = ecdsa.VerifyingKey.from_pem(s)
            else:
                vk = ecdsa.VerifyingKey.from_string(
                    bytes.fromhex(s), curve=self.curve)
        else:
            raise TypeError("peer_pubkey must be VerifyingKey, bytes, or str")

        priv = sk.privkey.secret_multiplier
        point = vk.pubkey.point * priv
        x = point.x()
        size = self.curve.baselen
        return x.to_bytes(size, 'big')
