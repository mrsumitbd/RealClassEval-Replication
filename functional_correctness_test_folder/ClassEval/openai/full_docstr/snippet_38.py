
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
        result = []
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                offset = ord('a')
                result.append(chr((ord(ch) - offset + shift) % 26 + offset))
            elif 'A' <= ch <= 'Z':
                offset = ord('A')
                result.append(chr((ord(ch) - offset + shift) % 26 + offset))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_cipher(self, plaintext):
        """
        Encrypts the plaintext using the Vigenere cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.vigenere_cipher("abc")
        'kfa'
        """
        result = []
        key = self.key
        key_len = len(key)
        key_indices = [ord(k.lower()) - ord('a') for k in key]
        key_pos = 0
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                offset = ord('a')
                shift = key_indices[key_pos % key_len]
                result.append(chr((ord(ch) - offset + shift) % 26 + offset))
                key_pos += 1
            elif 'A' <= ch <= 'Z':
                offset = ord('A')
                shift = key_indices[key_pos % key_len]
                result.append(chr((ord(ch) - offset + shift) % 26 + offset))
                key_pos += 1
            else:
                result.append(ch)
        return ''.join(result)

    def rail_fence_cipher(self, plain_text, rails):
        """
        Encrypts the plaintext using the Rail Fence cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.rail_fence_cipher("abc", 2)
        'acb'
        """
        if rails <= 1:
            return plain_text

        # Create rails
        rail = ['' for _ in range(rails)]
        current_row = 0
        direction = 1  # 1 for down, -1 for up

        for ch in plain_text:
            rail[current_row] += ch
            if current_row == 0:
                direction = 1
            elif current_row == rails - 1:
                direction = -1
            current_row += direction

        return ''.join(rail)
