
class BinaryDataProcessor:
    """
    This is a class used to process binary data, which includes functions such as clearing non 0 or 1 characters, counting binary string information, and converting to corresponding strings based on different encoding methods.
    """

    def __init__(self, binary_string):
        """
        Initialize the class with a binary string and clean it by removing all non 0 or 1 characters.
        """
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        """
        Clean the binary string by removing all non 0 or 1 characters.
        >>> bdp = BinaryDataProcessor("01101000daf3e4r01100101011011000110110001101111")
        >>> bdp.clean_non_binary_chars()
        >>> bdp.binary_string
        '0110100001100101011011000110110001101111'
        """
        self.binary_string = ''.join(
            c for c in self.binary_string if c in '01')

    def calculate_binary_info(self):
        """
        Calculate the binary string information, including the percentage of 0 and 1, and the total length of the binary string.
        >>> bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        >>> bdp.calculate_binary_info()
        {'Zeroes': 0.475, 'Ones': 0.525, 'Bit length': 40}
        """
        total = len(self.binary_string)
        if total == 0:
            return {'Zeroes': 0.0, 'Ones': 0.0, 'Bit length': 0}
        zeroes = self.binary_string.count('0')
        ones = self.binary_string.count('1')
        return {
            'Zeroes': round(zeroes / total, 3),
            'Ones': round(ones / total, 3),
            'Bit length': total
        }

    def convert_to_ascii(self):
        """
        Convert the binary string to ascii string.
        >>> bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        >>> bdp.convert_to_ascii()
        'hello'
        """
        chars = []
        s = self.binary_string
        for i in range(0, len(s) - len(s) % 8, 8):
            byte = s[i:i+8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars)

    def convert_to_utf8(self):
        """
        Convert the binary string to utf-8 string.
        >>> bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        >>> bdp.convert_to_utf8()
        'hello'
        """
        s = self.binary_string
        # Pad to multiple of 8
        if len(s) % 8 != 0:
            s = s[:-(len(s) % 8)]
        b = bytearray()
        for i in range(0, len(s), 8):
            byte = s[i:i+8]
            b.append(int(byte, 2))
        try:
            return b.decode('utf-8')
        except UnicodeDecodeError:
            return ''
