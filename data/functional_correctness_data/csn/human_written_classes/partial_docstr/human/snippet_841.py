class DigestSession:
    """Digest session"""

    def __init__(self, lib, session, mecha):
        self._lib = lib
        self._session = session
        self._mechanism = mecha.to_native()
        rv = self._lib.C_DigestInit(self._session, self._mechanism)
        if rv != CKR_OK:
            raise PyKCS11Error(rv)

    def update(self, data):
        """
        C_DigestUpdate

        :param data: data to add to the digest
        :type data: bytes or string
        """
        data1 = ckbytelist(data)
        rv = self._lib.C_DigestUpdate(self._session, data1)
        if rv != CKR_OK:
            raise PyKCS11Error(rv)
        return self

    def digestKey(self, handle):
        """
        C_DigestKey

        :param handle: key handle
        :type handle: CK_OBJECT_HANDLE
        """
        rv = self._lib.C_DigestKey(self._session, handle)
        if rv != CKR_OK:
            raise PyKCS11Error(rv)
        return self

    def final(self):
        """
        C_DigestFinal

        :return: the digest
        :rtype: ckbytelist
        """
        digest = ckbytelist()
        rv = self._lib.C_DigestFinal(self._session, digest)
        if rv != CKR_OK:
            raise PyKCS11Error(rv)
        rv = self._lib.C_DigestFinal(self._session, digest)
        if rv != CKR_OK:
            raise PyKCS11Error(rv)
        return digest