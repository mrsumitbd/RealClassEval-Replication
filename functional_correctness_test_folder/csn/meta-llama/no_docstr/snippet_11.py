
from Crypto.Cipher import AES


class AESModeCTR:

    def __init__(self, key, iv):
        """
        Initialize AES in CTR mode.

        :param key: The encryption key (16, 24, or 32 bytes).
        :param iv: The initialization vector (16 bytes).
        """
        self.key = key
        self.iv = iv
        self.cipher = AES.new(
            key, AES.MODE_CTR, nonce=iv[:8], initial_value=int.from_bytes(iv[8:], 'big'))

    def encrypt(self, data):
        """
        Encrypt data using AES in CTR mode.

        :param data: The data to be encrypted.
        :return: The encrypted data.
        """
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        """
        Decrypt data using AES in CTR mode.

        :param data: The data to be decrypted.
        :return: The decrypted data.
        """
        # In CTR mode, encryption and decryption are the same operation
        return self.cipher.decrypt(data)


# Example usage
if __name__ == "__main__":
    key = b'\x00' * 32  # 256-bit key
    iv = b'\x01' * 16   # 128-bit IV

    aes_ctr = AESModeCTR(key, iv)

    data = b'Hello, World!'
    encrypted_data = aes_ctr.encrypt(data)
    decrypted_data = aes_ctr.decrypt(encrypted_data)

    print(f"Original Data: {data}")
    print(f"Encrypted Data: {encrypted_data.hex()}")
    print(f"Decrypted Data: {decrypted_data}")
