class DecryptionUtils:
    """
    This is a class that provides methods for decryption, including the Caesar cipher, Vigenere cipher, and Rail Fence cipher.
    """

    def __init__(self, key):
        """
        Initializes the decryption utility with a key.
        :param key: The key to use for decryption,str.
        """
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        """
        Deciphers the given ciphertext using the Caesar cipher
        :param ciphertext: The ciphertext to decipher,str.
        :param shift: The shift to use for decryption,int.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.caesar_decipher('ifmmp', 1)
        'hello'

        """
        if not isinstance(ciphertext, str):
            raise TypeError("ciphertext must be a string")
        if not isinstance(shift, int):
            raise TypeError("shift must be an int")

        result = []
        shift = shift % 26
        for ch in ciphertext:
            if 'a' <= ch <= 'z':
                base = ord('a')
                val = (ord(ch) - base - shift) % 26
                result.append(chr(base + val))
            elif 'A' <= ch <= 'Z':
                base = ord('A')
                val = (ord(ch) - base - shift) % 26
                result.append(chr(base + val))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.vigenere_decipher('ifmmp')
        'ybocl'

        """
        if not isinstance(ciphertext, str):
            raise TypeError("ciphertext must be a string")
        if not isinstance(self.key, str) or len(self.key) == 0:
            raise ValueError("key must be a non-empty string")

        key_shifts = [(ord(k.lower()) - ord('a')) %
                      26 for k in self.key if k.isalpha()]
        if not key_shifts:
            raise ValueError(
                "key must contain at least one alphabetic character")

        result = []
        ki = 0
        for ch in ciphertext:
            if ch.isalpha():
                shift = key_shifts[ki % len(key_shifts)]
                if ch.islower():
                    base = ord('a')
                    val = (ord(ch) - base - shift) % 26
                    result.append(chr(base + val))
                else:
                    base = ord('A')
                    val = (ord(ch) - base - shift) % 26
                    result.append(chr(base + val))
                ki += 1
            else:
                result.append(ch)
        return ''.join(result)

    def rail_fence_decipher(self, encrypted_text, rails):
        """
        Deciphers the given ciphertext using the Rail Fence cipher
        :param encrypted_text: The ciphertext to decipher,str.
        :param rails: The number of rails to use for decryption,int.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.rail_fence_decipher('Hoo!el,Wrdl l', 3)
        'Hello, World!'

        """
        if not isinstance(encrypted_text, str):
            raise TypeError("encrypted_text must be a string")
        if not isinstance(rails, int):
            raise TypeError("rails must be an int")
        n = len(encrypted_text)
        if rails <= 1 or rails >= n:
            return encrypted_text

        # Determine rail pattern for positions
        pattern = []
        rail = 0
        direction = 1  # 1 down, -1 up
        for _ in range(n):
            pattern.append(rail)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

        # Count characters per rail
        counts = [0] * rails
        for r in pattern:
            counts[r] += 1

        # Slice the encrypted text to rails
        rails_chars = []
        idx = 0
        for count in counts:
            rails_chars.append(list(encrypted_text[idx:idx + count]))
            idx += count

        # Reconstruct plaintext by consuming from rails in pattern order
        pointers = [0] * rails
        result_chars = []
        for r in pattern:
            result_chars.append(rails_chars[r][pointers[r]])
            pointers[r] += 1

        return ''.join(result_chars)
