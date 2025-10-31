
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
        for c in ciphertext:
            if 'a' <= c <= 'z':
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(c)
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
        result = []
        key = self.key
        key_len = len(key)
        for i, c in enumerate(ciphertext):
            k = key[i % key_len]
            if 'a' <= c <= 'z':
                shift = ord(k.lower()) - ord('a')
                result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                shift = ord(k.upper()) - ord('A')
                result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(c)
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
        if rails == 1:
            return encrypted_text

        # Create the pattern of rails
        n = len(encrypted_text)
        rail_pattern = [0] * n
        rail = 0
        direction = 1
        for i in range(n):
            rail_pattern[i] = rail
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

        # Count how many letters in each rail
        rail_counts = [0] * rails
        for r in rail_pattern:
            rail_counts[r] += 1

        # Fill rails with the appropriate letters from encrypted_text
        rails_content = []
        idx = 0
        for count in rail_counts:
            rails_content.append(list(encrypted_text[idx:idx+count]))
            idx += count

        # Reconstruct the plaintext
        result = []
        rail_indices = [0] * rails
        for r in rail_pattern:
            result.append(rails_content[r][rail_indices[r]])
            rail_indices[r] += 1

        return ''.join(result)
