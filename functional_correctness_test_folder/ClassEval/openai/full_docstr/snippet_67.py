
import re


class NumericEntityUnescaper:
    """
    This is a class that provides functionality to replace numeric entities with their corresponding characters in a given string.
    """

    def __init__(self):
        # Precompile regex patterns for decimal and hexadecimal numeric entities
        self._decimal_pattern = re.compile(r'&#(\d+);')
        self._hex_pattern = re.compile(r'&#x([0-9a-fA-F]+);')

    def replace(self, string):
        """
        Replaces numeric character references (HTML entities) in the input string with their corresponding Unicode characters.
        :param string: str, the input string containing numeric character references.
        :return: str, the input string with numeric character references replaced with their corresponding Unicode characters.
        >>> unescaper = NumericEntityUnescaper()
        >>> unescaper.replace("&#65;&#66;&#67;")
        'ABC'
        """
        if not isinstance(string, str):
            raise TypeError("Input must be a string")

        # First replace hexadecimal entities
        def _hex_repl(match):
            hex_value = match.group(1)
            try:
                codepoint = int(hex_value, 16)
                return chr(codepoint)
            except (ValueError, OverflowError):
                # If conversion fails, return the original match unchanged
                return match.group(0)

        result = self._hex_pattern.sub(_hex_repl, string)

        # Then replace decimal entities
        def _dec_repl(match):
            dec_value = match.group(1)
            try:
                codepoint = int(dec_value, 10)
                return chr(codepoint)
            except (ValueError, OverflowError):
                return match.group(0)

        result = self._decimal_pattern.sub(_dec_repl, result)

        return result

    @staticmethod
    def is_hex_char(char):
        """
        Determines whether a given character is a hexadecimal digit.
        :param char: str, the character to check.
        :return: bool, True if the character is a hexadecimal digit, False otherwise.
        >>> NumericEntityUnescaper.is_hex_char('a')
        True
        """
        if not isinstance(char, str) or len(char) != 1:
            return False
        return char.isdigit() or ('a' <= char.lower() <= 'f')
