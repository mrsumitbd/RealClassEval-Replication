
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
        """
        if isinstance(x, float):
            integer_part, decimal_part = str(x).split('.')
            return self.format_string(integer_part) + " AND " + self.trans_two(decimal_part) + " ONLY"
        else:
            return self.format_string(str(x)) + " ONLY"

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        """
        parts = []
        length = len(x)
        for i in range(0, length, 3):
            part = x[max(0, length - i - 3):length - i]
            if part != "000":
                parts.append(self.trans_three(part) +
                             " " + self.parse_more(i // 3))
        return " ".join(reversed(parts)).strip()

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        """
        if len(s) == 1:
            s = "0" + s
        if s[0] == '1':
            return self.NUMBER_TEEN[int(s[1])]
        elif s[0] == '0':
            return self.NUMBER[int(s[1])]
        else:
            return self.NUMBER_TEN[int(s[0]) - 1] + (" " + self.NUMBER[int(s[1])] if s[1] != '0' else "")

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        """
        if len(s) == 1:
            s = "00" + s
        elif len(s) == 2:
            s = "0" + s
        hundred = self.NUMBER[int(s[0])] + " HUNDRED" if s[0] != '0' else ""
        tens_and_units = self.trans_two(s[1:])
        if hundred and tens_and_units:
            return hundred + " AND " + tens_and_units
        elif hundred:
            return hundred
        else:
            return tens_and_units

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        """
        return self.NUMBER_MORE[i]
