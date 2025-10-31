
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
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                ascii_offset = 97 if char.islower() else 65
                plaintext += chr((ord(char) - ascii_offset -
                                 shift) % 26 + ascii_offset)
            else:
                plaintext += char
        return plaintext

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.vigenere_decipher('ifmmp')
        'ybocl'

        """
        key = self.key.lower()
        key_index = 0
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                ascii_offset = 97 if char.islower() else 65
                shift = ord(key[key_index % len(key)]) - 97
                plaintext += chr((ord(char) - ascii_offset -
                                 shift) % 26 + ascii_offset)
                key_index += 1
            else:
                plaintext += char
        return plaintext

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

        # Create a list to store the characters in each rail
        rail = [''] * rails
        # Initialize variables to keep track of the current rail and direction
        dir = 0  # 0: down, 1: up
        rail_index = 0

        # Distribute the characters of the encrypted text into the rails
        for char in encrypted_text:
            rail[rail_index] += char
            if rail_index == 0:
                dir = 0
            elif rail_index == rails - 1:
                dir = 1
            rail_index += 1 if dir == 0 else -1

        # Reconstruct the plaintext by reading the characters from the rails in the correct order
        plaintext = ''
        dir = 0
        rail_index = 0
        rail_lengths = [len(r) for r in rail]
        rail_pointers = [0] * rails
        for _ in range(len(encrypted_text)):
            plaintext += rail[rail_index][rail_pointers[rail_index]]
            rail_pointers[rail_index] += 1
            if rail_index == 0:
                dir = 0
            elif rail_index == rails - 1:
                dir = 1
            rail_index += 1 if dir == 0 else -1

        return plaintext
