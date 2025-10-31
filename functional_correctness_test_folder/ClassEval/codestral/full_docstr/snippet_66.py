
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
        if isinstance(x, float):
            integer_part, decimal_part = str(x).split('.')
            integer_words = self.format(int(integer_part))
            decimal_words = self.format(int(decimal_part))
            return f"{integer_words} POINT {decimal_words} ONLY"
        else:
            s = str(x)
            if len(s) > 15:
                return "NUMBER TOO LARGE"
            s = s.zfill(15)
            result = []
            pos = 0
            while pos < len(s):
                s4 = s[pos:pos+3]
                n4 = int(s4)
                if n4:
                    result.append(self.trans_three(s4))
                    result.append(self.parse_more((len(s)-pos-1)//3))
                pos += 3
            return ' '.join(result) + " ONLY"

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        if '.' in x:
            integer_part, decimal_part = x.split('.')
            integer_words = self.format_string(integer_part)
            decimal_words = self.format_string(decimal_part)
            return f"{integer_words} POINT {decimal_words} ONLY"
        else:
            return self.format(int(x))

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        ten, unit = map(int, s)
        if ten == 1:
            return self.NUMBER_TEEN[unit]
        else:
            return self.NUMBER_TEN[ten-1] + (" " + self.NUMBER[unit] if unit else "")

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        hundred, ten, unit = map(int, s)
        result = []
        if hundred:
            result.append(self.NUMBER[hundred] + " HUNDRED")
        if ten or unit:
            result.append("AND")
            result.append(self.trans_two(s[1:]))
        return ' '.join(result)

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
