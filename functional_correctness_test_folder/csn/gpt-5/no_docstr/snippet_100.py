class Client:
    def __init__(self, device):
        if device is None:
            raise ValueError("device must not be None")
        self._device = device

    def pubkey(self, identity, ecdh=False):
        # Preferred: device.pubkey(identity, ecdh=False)
        if hasattr(self._device, "pubkey"):
            try:
                return self._device.pubkey(identity, ecdh=ecdh)
            except TypeError:
                # Some implementations may not use keyword
                return self._device.pubkey(identity, ecdh)
        # Alternative names
        for method_name in ("get_pubkey", "public_key", "get_public_key"):
            if hasattr(self._device, method_name):
                meth = getattr(self._device, method_name)
                try:
                    return meth(identity, ecdh=ecdh)
                except TypeError:
                    try:
                        return meth(identity, ecdh)
                    except TypeError:
                        return meth(identity)
        raise NotImplementedError(
            "Underlying device does not expose a public key retrieval method")

    def ecdh(self, identity, peer_pubkey):
        # Preferred: device.ecdh(identity, peer_pubkey)
        if hasattr(self._device, "ecdh"):
            return self._device.ecdh(identity, peer_pubkey)
        # Alternative names
        for method_name in (
            "derive",
            "derive_shared",
            "shared_secret",
            "compute_shared",
            "compute_shared_secret",
            "derive_key",
        ):
            if hasattr(self._device, method_name):
                return getattr(self._device, method_name)(identity, peer_pubkey)
        raise NotImplementedError(
            "Underlying device does not expose an ECDH method")
