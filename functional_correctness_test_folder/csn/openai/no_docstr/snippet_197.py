
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class RSAOAEPMechanism:
    """
    Wrapper for RSA OAEP padding mechanism.

    Parameters
    ----------
    hashAlg : type
        A hash algorithm class from cryptography.hazmat.primitives.hashes
        (e.g., hashes.SHA256).
    mgf : type
        A mask generation function class from cryptography.hazmat.primitives.asymmetric.padding
        (e.g., padding.MGF1).
    label : bytes, optional
        Optional label for OAEP padding. Defaults to None.
    """

    def __init__(self, hashAlg, mgf, label=None):
        if not isinstance(label, (bytes, type(None))):
            raise TypeError("label must be bytes or None")
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.label = label

    def to_native(self):
        """
        Convert to the native cryptography OAEP padding object.

        Returns
        -------
        cryptography.hazmat.primitives.asymmetric.padding.OAEP
        """
        # Instantiate the hash algorithm
        hash_instance = self.hashAlg()
        # Instantiate the MGF with the same hash algorithm
        mgf_instance = self.mgf(hash_instance)
        # Create the OAEP padding object
        return padding.OAEP(
            mgf=mgf_instance,
            algorithm=hash_instance,
            label=self.label
        )
