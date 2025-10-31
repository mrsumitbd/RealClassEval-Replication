
class NumberWordFormatter:
    """
    This is a class that provides to convert numbers into their corresponding English word representation,
    including handling the conversion of both the integer and decimal parts, and incorporating appropriate
    connectors and units.
    """

    def __init__(self):
        """
        Initialize NumberWordFormatter object.
        """
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR",
                       "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN",
                            "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY",
                           "SEVENTY", "EIGHTY", "NINETY"]
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
        if isinstance(x, str):
            return self.format_string(x)

        # Handle negative numbers
        negative = False
        if isinstance(x, (int, float)) and x < 0:
            negative = True
            x = -x

        # Separate integer and decimal parts
        if isinstance(x, float):
            int_part = int(x)
            dec_part = str(x).split('.')[1]
        else:
            int_part = int(x)
            dec_part = None

        # Convert integer part
        if int_part == 0:
            int_words = "ZERO"
        else:
            int_words = self._convert_integer(int_part)

        # Convert decimal part
        if dec_part:
            dec_words = " POINT " + \
                " ".join(self.NUMBER[int(d)] for d in dec_part)
        else:
            dec_words = ""

        result = (("NEGATIVE " if negative else "") +
                  int_words + dec_words + " ONLY").strip()
        return result

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        # Remove commas and spaces
        clean = x.replace(',', '').strip()
        if not clean:
            raise ValueError("Empty string cannot be converted")
        # Determine if float
        if '.' in clean:
            try:
                val = float(clean)
            except ValueError:
                raise ValueError(f"Invalid numeric string: {x}")
        else:
            try:
                val = int(clean)
            except ValueError:
                raise ValueError(f"Invalid numeric string: {x}")
        return self.format(val)

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        if len(s) != 2 or not s.isdigit():
            raise ValueError("trans_two expects a two-digit string")
        first, second = int(s[0]), int(s[1])
        if first == 0:
            return self.NUMBER[second]
        if first == 1:
            return self.NUMBER_TEEN[second]
        if second == 0:
            return self.NUMBER_TEN[first]
        return f"{self.NUMBER_TEN[first]} {self.NUMBER[second]}"

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        if len(s) != 3 or not s.isdigit():
            raise ValueError("trans_three expects a three-digit string")
        first, second, third = int(s[0]), int(s[1]), int(s[2])
        if first == 0:
            return self.trans_two(s[1:])
        words = f"{self.NUMBER[first]} HUNDRED"
        if second == 0 and third == 0:
            return words
        words += " AND " + self.trans_two(s[1:])
        return words

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if i < 0 or i >= len(self.NUMBER_MORE):
            return ""
        return self.NUMBER_MORE[i]

    # Helper method to convert integer part
    def _convert_integer(self, n):
        groups = []
        while n > 0:
            groups.append(n % 1000)
            n //= 1000
        words = []
        for idx, grp in enumerate(groups):
            if grp == 0:
                continue
            grp_str = f"{grp:03d}"
            grp_words = self.trans_three(grp_str)
            suffix = self.parse_more(idx)
            if suffix:
                grp_words += f" {suffix}"
            words.append(grp_words)
        return " ".join(reversed(words))
