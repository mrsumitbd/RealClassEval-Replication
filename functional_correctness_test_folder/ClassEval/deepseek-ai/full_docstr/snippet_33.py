
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
        plaintext = []
        for char in ciphertext:
            if char.isalpha():
                shifted = ord(char) - shift
                if char.islower():
                    if shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted < ord('A'):
                        shifted += 26
                plaintext.append(chr(shifted))
            else:
                plaintext.append(char)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.vigenere_decipher('ifmmp')
        'ybocl'
        """
        plaintext = []
        key_repeated = (
            self.key * ((len(ciphertext) // len(self.key)) + 1))[:len(ciphertext)]
        for i in range(len(ciphertext)):
            cipher_char = ciphertext[i]
            key_char = key_repeated[i]
            if cipher_char.isalpha():
                shift = ord(key_char.lower()) - ord('a')
                decrypted_char = ord(cipher_char.lower()) - shift
                if decrypted_char < ord('a'):
                    decrypted_char += 26
                plaintext.append(chr(decrypted_char))
            else:
                plaintext.append(cipher_char)
        return ''.join(plaintext)

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

        pattern = []
        for i in range(rails):
            pattern.append([])

        down = False
        row = 0

        for i in range(len(encrypted_text)):
            pattern[row].append(i)
            if row == 0 or row == rails - 1:
                down = not down
            row += 1 if down else -1

        indices = []
        for i in range(rails):
            indices.extend(pattern[i])

        result = [''] * len(encrypted_text)
        for i, pos in enumerate(indices):
            result[pos] = encrypted_text[i]

        return ''.join(result)
