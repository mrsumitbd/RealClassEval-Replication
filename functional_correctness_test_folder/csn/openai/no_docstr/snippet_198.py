
# rsa_pss_mechanism.py

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class RSA_PSS_Mechanism:
    """
    A lightweight wrapper that represents an RSA-PSS signing or verification
    mechanism.  It stores the chosen hash algorithm, mask generation function
    (MGF) and salt length, and can produce a native `cryptography` padding
    object via :meth:`to_native`.

    Parameters
    ----------
    mecha : str
        The mechanism name (currently only 'PSS' is supported).
    hashAlg : str
        The hash algorithm name, e.g. 'SHA256', 'SHA512', etc.
    mgf : str
        The mask generation function name.  Only 'MGF1' is supported.
    sLen : int
        The salt length in bytes.  Use ``padding.PSS.MAX_LENGTH`` for the
        maximum allowed value.
    """

    _HASH_ALG_MAP = {
        'SHA1': hashes.SHA1,
        'SHA224': hashes.SHA224,
        'SHA256': hashes.SHA256,
        'SHA384': hashes.SHA384,
        'SHA512': hashes.SHA512,
        'SHA3_224': hashes.SHA3_224,
        'SHA3_256': hashes.SHA3_256,
        'SHA3_384': hashes.SHA3_384,
        'SHA3_512': hashes.SHA3_512,
    }

    _MGF_MAP = {
        'MGF1': padding.MGF1,
    }

    def __init__(self, mecha, hashAlg, mgf, sLen):
        if mecha.upper() != 'PSS':
            raise ValueError(
                f"Unsupported mechanism '{mecha}'. Only 'PSS' is supported.")
        self.mecha = mecha.upper()

        hash_cls = self._HASH_ALG_MAP.get(hashAlg.upper())
        if hash_cls is None:
            raise ValueError(f"Unsupported hash algorithm '{hashAlg}'.")
        self.hash_alg = hash_cls()

        mgf_cls = self._MGF_MAP.get(mgf.upper())
        if mgf_cls is None:
            raise ValueError(f"Unsupported MGF '{mgf}'.")
        self.mgf = mgf_cls(self.hash_alg)

        if not isinstance(sLen, int) or sLen < 0:
            raise ValueError(
                f"Salt length must be a non‑negative integer, got {sLen}.")
        self.sLen = sLen

    def to_native(self):
        """
        Return a native `cryptography` padding.PSS object configured with the
        stored parameters.

        Returns
        -------
        cryptography.hazmat.primitives.asymmetric.padding.PSS
        """
        return padding.PSS(
            mgf=self.mgf,
            salt_length=self.sLen
        )
