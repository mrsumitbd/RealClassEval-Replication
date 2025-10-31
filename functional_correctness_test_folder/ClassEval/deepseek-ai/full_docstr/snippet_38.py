
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
        ciphertext = []
        for char in plaintext:
            if char.islower():
                shifted = ord(char) - ord('a')
                shifted = (shifted + shift) % 26
                ciphertext.append(chr(shifted + ord('a')))
            elif char.isupper():
                shifted = ord(char) - ord('A')
                shifted = (shifted + shift) % 26
                ciphertext.append(chr(shifted + ord('A')))
            else:
                ciphertext.append(char)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plaintext):
        """
        Encrypts the plaintext using the Vigenere cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.vigenere_cipher("abc")
        'kfa'

        """
        ciphertext = []
        key_repeated = (
            self.key * ((len(plaintext) // len(self.key)) + 1))[:len(plaintext)]
        for i in range(len(plaintext)):
            plain_char = plaintext[i]
            key_char = key_repeated[i]
            if plain_char.islower():
                plain_num = ord(plain_char) - ord('a')
                key_num = ord(key_char.lower()) - ord('a')
                cipher_num = (plain_num + key_num) % 26
                ciphertext.append(chr(cipher_num + ord('a')))
            elif plain_char.isupper():
                plain_num = ord(plain_char) - ord('A')
                key_num = ord(key_char.upper()) - ord('A')
                cipher_num = (plain_num + key_num) % 26
                ciphertext.append(chr(cipher_num + ord('A')))
            else:
                ciphertext.append(plain_char)
        return ''.join(ciphertext)

    def rail_fence_cipher(self, plain_text, rails):
        """
        Encrypts the plaintext using the Rail Fence cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.rail_fence_cipher("abc", 2)
        'acb'

        """
        if rails == 1:
            return plain_text
        rail = [[] for _ in range(rails)]
        direction = 1
        current_rail = 0
        for char in plain_text:
            rail[current_rail].append(char)
            current_rail += direction
            if current_rail == rails - 1 or current_rail == 0:
                direction *= -1
        ciphertext = []
        for r in rail:
            ciphertext.extend(r)
        return ''.join(ciphertext)
