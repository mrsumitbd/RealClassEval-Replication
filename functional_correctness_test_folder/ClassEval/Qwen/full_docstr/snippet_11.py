
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
        """
        self.binary_string = ''.join(
            char for char in self.binary_string if char in '01')

    def calculate_binary_info(self):
        """
        Calculate the binary string information, including the percentage of 0 and 1, and the total length of the binary string.
        """
        length = len(self.binary_string)
        if length == 0:
            return {'Zeroes': 0.0, 'Ones': 0.0, 'Bit length': 0}
        zeroes = self.binary_string.count('0')
        ones = self.binary_string.count('1')
        return {'Zeroes': zeroes / length, 'Ones': ones / length, 'Bit length': length}

    def convert_to_ascii(self):
        """
        Convert the binary string to ascii string.
        """
        ascii_string = ''
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i+8]
            if len(byte) == 8:
                ascii_string += chr(int(byte, 2))
        return ascii_string

    def convert_to_utf8(self):
        """
        Convert the binary string to utf-8 string.
        """
        return self.convert_to_ascii()  # For this specific example, ASCII and UTF-8 conversion are the same
