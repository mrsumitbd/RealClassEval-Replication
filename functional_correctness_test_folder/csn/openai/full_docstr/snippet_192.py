
# -*- coding: utf-8 -*-

"""
Implementation of the CKM_CONCATENATE_BASE_AND_KEY key derivation mechanism.
"""

# Try to import the PKCS#11 constants and structures from PyKCS11.
# If PyKCS11 is not available, fall back to a minimal representation.
try:
    from PyKCS11.LowLevel import (
        CKM_CONCATENATE_BASE_AND_KEY,
        CK_CONCATENATE_BASE_AND_KEY_PARAMS,
    )
except Exception:  # pragma: no cover
    CKM_CONCATENATE_BASE_AND_KEY = "CKM_CONCATENATE_BASE_AND_KEY"

    class CK_CONCATENATE_BASE_AND_KEY_PARAMS:
        """
        Minimal stand‑in for the PyKCS11 CK_CONCATENATE_BASE_AND_KEY_PARAMS
        structure.  It simply stores the base key handle and the key data.
        """

        def __init__(self, base_key, key_data):
            self.base_key = base_key
            self.key_data = key_data

        def __repr__(self):
            return (
                f"CK_CONCATENATE_BASE_AND_KEY_PARAMS("
                f"base_key={self.base_key!r}, key_data={self.key_data!r})"
            )


class CONCATENATE_BASE_AND_KEY_Mechanism:
    """CKM_CONCATENATE_BASE_AND_KEY key derivation mechanism"""

    def __init__(self, encKey):
        """
        :param encKey: a handle of encryption key
        """
        self.encKey = encKey

    def to_native(self):
        """
        Convert the mechanism to the native format expected by the PKCS#11
        library.  The native format is a tuple of the mechanism type and a
        CK_CONCATENATE_BASE_AND_KEY_PARAMS instance.
        """
        # The key data is not provided in this context; use None.
        params = CK_CONCATENATE_BASE_AND_KEY_PARAMS(self.encKey, None)
        return (CKM_CONCATENATE_BASE_AND_KEY, params)
