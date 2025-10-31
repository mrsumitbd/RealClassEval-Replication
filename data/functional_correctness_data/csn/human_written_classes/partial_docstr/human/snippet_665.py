class BaseHSM:

    def certificate(self):
        """
        callback for HSM
        used to identfy the ssh agents key exports via fingerprint

        :return: public-key-fingerprint, certificate-in-pem
        """
        raise NotImplementedError()

    def sign(self, keyid, data, mech):
        """
        sign

        :param keyid: the keyid as returned by certificate()
        :param data:
        :param mech: hash algo
        :return: PKCS7 signature blob
        """
        raise NotImplementedError()