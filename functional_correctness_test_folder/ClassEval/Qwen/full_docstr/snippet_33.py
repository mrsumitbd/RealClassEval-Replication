
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
                shift_amount = shift % 26
                if char.islower():
                    new_char = chr((ord(char) - shift_amount - 97) % 26 + 97)
                else:
                    new_char = chr((ord(char) - shift_amount - 65) % 26 + 65)
                plaintext.append(new_char)
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
        key_length = len(self.key)
        key_as_int = [ord(i) for i in self.key]
        ciphertext_int = [ord(i) for i in ciphertext]
        plaintext = ''
        for i in range(len(ciphertext_int)):
            if ciphertext[i].isalpha():
                value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
                if ciphertext[i].islower():
                    plaintext += chr(value + 97)
                else:
                    plaintext += chr(value + 65)
            else:
                plaintext += ciphertext[i]
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

        rail_fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1

        for char in encrypted_text:
            rail_fence[rail] += char
            rail += direction

            if rail == 0 or rail == rails - 1:
                direction *= -1

        rail_lengths = [len(rail_fence[i]) for i in range(rails)]
        rail_indices = [0] * rails
        plaintext = ''

        for char in encrypted_text:
            for rail in range(rails):
                if rail_indices[rail] < rail_lengths[rail]:
                    if rail_fence[rail][rail_indices[rail]] == char:
                        plaintext += char
                        rail_indices[rail] += 1
                        break

        return plaintext
