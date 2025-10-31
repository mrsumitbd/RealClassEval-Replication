
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class AESModeCTR:
    """
    AES encryption/decryption in CTR mode.

    Parameters
    ----------
    key : bytes
        The AES key. Must be 16, 24, or 32 bytes long.
    iv : bytes
        The initial counter value (nonce). Must be 16 bytes long.
    """

    def __init__(self, key: bytes, iv: bytes):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes")
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes")
        if len(key) not in (16, 24, 32):
            raise ValueError("key must be 16, 24, or 32 bytes long")
        if len(iv) != 16:
            raise ValueError("iv must be 16 bytes long")

        self._key = bytes(key)
        self._iv = bytes(iv)
        self._backend = default_backend()
        self._cipher = Cipher(algorithms.AES(self._key),
                              modes.CTR(self._iv), backend=self._backend)

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data using AES-CTR.

        Parameters
        ----------
        data : bytes
            Plaintext data to encrypt.

        Returns
        -------
        bytes
            Ciphertext.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        encryptor = self._cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt data using AES-CTR.

        Parameters
        ----------
        data : bytes
            Ciphertext data to decrypt.

        Returns
        -------
        bytes
            Plaintext.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        decryptor = self._cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()
