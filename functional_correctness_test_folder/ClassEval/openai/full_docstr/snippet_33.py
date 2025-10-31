
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
        result = []
        for ch in ciphertext:
            if 'a' <= ch <= 'z':
                offset = ord('a')
                result.append(chr((ord(ch) - offset - shift) % 26 + offset))
            elif 'A' <= ch <= 'Z':
                offset = ord('A')
                result.append(chr((ord(ch) - offset - shift) % 26 + offset))
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
        key = self.key
        key_len = len(key)
        result = []
        for i, ch in enumerate(ciphertext):
            if 'a' <= ch <= 'z':
                offset = ord('a')
                k = ord(key[i % key_len].lower()) - offset
                result.append(chr((ord(ch) - offset - k) % 26 + offset))
            elif 'A' <= ch <= 'Z':
                offset = ord('A')
                k = ord(key[i % key_len].upper()) - offset
                result.append(chr((ord(ch) - offset - k) % 26 + offset))
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
        if rails <= 1 or rails >= len(encrypted_text):
            return encrypted_text

        # Determine the rail pattern for each character position
        pattern = []
        rail = 0
        direction = 1  # 1 for down, -1 for up
        for _ in range(len(encrypted_text)):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        # Count how many chars per rail
        rail_counts = [0] * rails
        for r in pattern:
            rail_counts[r] += 1

        # Allocate positions for each rail
        rail_positions = []
        idx = 0
        for count in rail_counts:
            rail_positions.append(list(range(idx, idx + count)))
            idx += count

        # Fill rails with characters from encrypted_text
        rails_matrix = [''] * rails
        pos_indices = [0] * rails
        for i, ch in enumerate(encrypted_text):
            r = pattern[i]
            pos = rail_positions[r][pos_indices[r]]
            rails_matrix[r] = rails_matrix[r] + ch
            pos_indices[r] += 1

        # Reconstruct plaintext by traversing the pattern again
        result = []
        pos_indices = [0] * rails
        for r in pattern:
            result.append(rails_matrix[r][pos_indices[r]])
            pos_indices[r] += 1

        return ''.join(result)
