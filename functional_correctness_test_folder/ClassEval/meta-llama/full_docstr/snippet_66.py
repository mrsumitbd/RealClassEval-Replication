
class NumberWordFormatter:
    """
    This is a class that provides to convert numbers into their corresponding English word representation, including handling the conversion of both the integer and decimal parts, and incorporating appropriate connectors and units.
    """

    def __init__(self):
        """
        Initialize NumberWordFormatter object.
        """
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR",
                       "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
                            "EIGHTEEN",
                            "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY",
                           "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
        self.NUMBER_SUFFIX = ["k", "w", "", "m", "", "",
                              "b", "", "", "t", "", "", "p", "", "", "e"]

    def format(self, x):
        """
        Converts a number into words format
        :param x: int or float, the number to be converted into words format
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format(123456)
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        return self.format_string(str(x))

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        parts = x.split('.')
        integer_part = parts[0]
        if len(parts) > 1:
            decimal_part = parts[1]
        else:
            decimal_part = ''

        integer_part_in_words = self.convert_integer(integer_part)
        if decimal_part:
            decimal_part_in_words = self.convert_decimal(decimal_part)
            return f"{integer_part_in_words} POINT {decimal_part_in_words} ONLY"
        else:
            return f"{integer_part_in_words} ONLY"

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        if int(s) < 10:
            return self.NUMBER[int(s)]
        elif int(s) < 20:
            return self.NUMBER_TEEN[int(s) - 10]
        else:
            if s[1] == '0':
                return self.NUMBER_TEN[int(s[0]) - 1]
            else:
                return f"{self.NUMBER_TEN[int(s[0]) - 1]} {self.NUMBER[int(s[1])]}"

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        if int(s) == 0:
            return ''
        elif s[0] == '0':
            return self.trans_two(s[1:])
        else:
            if int(s[1:]) == 0:
                return f"{self.NUMBER[int(s[0])]} HUNDRED"
            else:
                return f"{self.NUMBER[int(s[0])]} HUNDRED AND {self.trans_two(s[1:])}"

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        return self.NUMBER_MORE[i]

    def convert_integer(self, s):
        s = s.lstrip('0')
        if not s:
            return 'ZERO'
        result = ''
        i = 0
        while s:
            if len(s) % 3 != 0:
                s = '0' * (3 - len(s) % 3) + s
            part = s[-3:]
            s = s[:-3]
            part_in_words = self.trans_three(part)
            if part_in_words:
                if i > 0:
                    result = f"{part_in_words} {self.parse_more(i)} {result}"
                else:
                    result = part_in_words
            i += 1
        return result.strip()

    def convert_decimal(self, s):
        result = ''
        for digit in s:
            if digit != '0':
                result += f" {self.NUMBER[int(digit)]}"
            else:
                result += ' ZERO'
        return result.strip()
