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
        def shift_char(c, s):
            if 'a' <= c <= 'z':
                base = ord('a')
                return chr((ord(c) - base + s) % 26 + base)
            if 'A' <= c <= 'Z':
                base = ord('A')
                return chr((ord(c) - base + s) % 26 + base)
            return c

        s = shift % 26
        return ''.join(shift_char(ch, s) for ch in plaintext)

    def vigenere_cipher(self, plaintext):
        """
        Encrypts the plaintext using the Vigenere cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.vigenere_cipher("abc")
        'kfa'

        """
        if not self.key:
            return plaintext
        key_shifts = [(ord(c.lower()) - ord('a')) %
                      26 for c in self.key if c.isalpha()]
        if not key_shifts:
            return plaintext

        res = []
        ki = 0
        klen = len(key_shifts)

        for ch in plaintext:
            if ch.isalpha():
                shift = key_shifts[ki % klen]
                if 'a' <= ch <= 'z':
                    base = ord('a')
                    res.append(chr((ord(ch) - base + shift) % 26 + base))
                else:
                    base = ord('A')
                    res.append(chr((ord(ch) - base + shift) % 26 + base))
                ki += 1
            else:
                res.append(ch)
        return ''.join(res)

    def rail_fence_cipher(self, plain_text, rails):
        """
        Encrypts the plaintext using the Rail Fence cipher.
        :param plaintext: The plaintext to encrypt, str.
        :return: The ciphertext, str.
        >>> e = EncryptionUtils("key")
        >>> e.rail_fence_cipher("abc", 2)
        'acb'

        """
        if rails <= 1 or rails >= len(plain_text):
            return plain_text

        # Initialize rails
        fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1  # 1 down, -1 up

        for ch in plain_text:
            fence[rail] += ch
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

        return ''.join(fence)
