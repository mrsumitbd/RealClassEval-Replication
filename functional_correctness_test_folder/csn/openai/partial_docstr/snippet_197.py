
from PyKCS11.LowLevel import (
    CKM_RSA_PKCS_OAEP,
    CK_RSA_PKCS_OAEP_PARAMS,
    CKZ_DATA_SPECIFIED,
)


class RSAOAEPMechanism:
    def __init__(self, hashAlg, mgf, label=None):
        """
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        """
        self.hashAlg = hashAlg
        self.mgf = mgf
        if label is not None and not isinstance(label, (bytes, bytearray)):
            # Accept string labels and encode them as UTF‑8
            label = label.encode("utf-8")
        self.label = label

    def to_native(self):
        """Convert mechanism to native format."""
        if self.label:
            source = CKZ_DATA_SPECIFIED
            pSourceData = self.label
            ulSourceDataLen = len(self.label)
        else:
            source = CKZ_DATA_SPECIFIED
            pSourceData = None
            ulSourceDataLen = 0

        params = CK_RSA_PKCS_OAEP_PARAMS(
            hashAlg=self.hashAlg,
            mgf=self.mgf,
            source=source,
            pSourceData=pSourceData,
            ulSourceDataLen=ulSourceDataLen,
        )
        return (CKM_RSA_PKCS_OAEP, params)
