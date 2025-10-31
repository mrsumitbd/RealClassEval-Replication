
class EncryptionUtils:
    """
    This is a class that provides methods for encryption, including the Caesar cipher, Vigenere cipher, and Rail Fence cipher.
    """

    def __init__(self, key):
        """
        Initializes the class with a key.
        :param key: The key to use for encryption, str.
        """
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        """
        Encrypts the plaintext using the Caesar cipher.
        :param plaintext: The plaintext to encrypt, str.
        :param shift: The number of characters to shift each character in the plaintext, int.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.caesar_cipher("abc", 1)
        'bcd'

        """
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                ciphertext += chr((ord(char) - ascii_offset +
                                  shift) % 26 + ascii_offset)
            else:
                ciphertext += char
        return ciphertext

    def vigenere_cipher(self, plaintext):
        """
        Encrypts the plaintext using the Vigenere cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.vigenere_cipher("abc")
        'kfa'

        """
        ciphertext = ""
        key_index = 0
        key = self.key.lower()
        for char in plaintext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shift = ord(key[key_index % len(key)]) - 97
                ciphertext += chr((ord(char) - ascii_offset +
                                  shift) % 26 + ascii_offset)
                key_index += 1
            else:
                ciphertext += char
        return ciphertext

    def rail_fence_cipher(self, plain_text, rails):
        """
        Encrypts the plaintext using the Rail Fence cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.rail_fence_cipher("abc", 2)
        'acb'

        """
        if rails == 1 or rails >= len(plain_text):
            return plain_text

        fence = [[] for _ in range(rails)]
        dir = 0  # 0: down, 1: up
        rail = 0

        for char in plain_text:
            fence[rail].append(char)
            if rail == 0:
                dir = 0
            elif rail == rails - 1:
                dir = 1

            rail += -1 if dir else 1

        ciphertext = ''.join(''.join(rail) for rail in fence)
        return ciphertext
