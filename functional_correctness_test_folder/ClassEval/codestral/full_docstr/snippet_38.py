
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
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                ciphertext += chr(shifted)
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
        ciphertext = []
        key_length = len(self.key)
        for i, char in enumerate(plaintext):
            if char.isalpha():
                key_char = self.key[i % key_length]
                key_shift = ord(key_char.lower()) - ord('a')
                if char.islower():
                    shifted = ord(char) - ord('a')
                    shifted = (shifted + key_shift) % 26
                    ciphertext.append(chr(shifted + ord('a')))
                elif char.isupper():
                    shifted = ord(char) - ord('A')
                    shifted = (shifted + key_shift) % 26
                    ciphertext.append(chr(shifted + ord('A')))
            else:
                ciphertext.append(char)
        return ''.join(ciphertext)

    def rail_fence_cipher(self, plaintext, rails):
        """
        Encrypts the plaintext using the Rail Fence cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.rail_fence_cipher("abc", 2)
        'acb'
        """
        if rails == 1:
            return plaintext
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        ciphertext = []
        for rail in fence:
            ciphertext.extend(rail)
        return ''.join(ciphertext)
