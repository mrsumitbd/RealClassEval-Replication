class NumericEntityUnescaper:
    """
    This is a class that provides functionality to replace numeric entities with their corresponding characters in a given string.
    """

    def __init__(self):
        pass

    def replace(self, string):
        """
        Replaces numeric character references (HTML entities) in the input string with their corresponding Unicode characters.
        :param string: str, the input string containing numeric character references.
        :return: str, the input string with numeric character references replaced with their corresponding Unicode characters.
        >>> unescaper = NumericEntityUnescaper()
        >>> unescaper.replace("&#65;&#66;&#67;")
        'ABC'

        """
        import re

        if not isinstance(string, str):
            raise TypeError("Input must be a string")

        pattern = re.compile(r'&#(x[0-9A-Fa-f]+|\d+);')

        def _replace_match(m):
            s = m.group(1)
            try:
                if s[0] in ('x', 'X'):
                    cp = int(s[1:], 16)
                else:
                    cp = int(s, 10)
                if 0 <= cp <= 0x10FFFF and not (0xD800 <= cp <= 0xDFFF):
                    return chr(cp)
            except Exception:
                pass
            return m.group(0)

        return pattern.sub(_replace_match, string)

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
        c = char
        return ('0' <= c <= '9') or ('a' <= c <= 'f') or ('A' <= c <= 'F')
