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
        from decimal import Decimal, InvalidOperation

        if isinstance(x, bool):
            raise ValueError("Invalid input type")

        if isinstance(x, int):
            return self.format_string(str(x))
        elif isinstance(x, float):
            # Avoid binary float artifacts
            return self.format_string(str(Decimal(str(x))))
        else:
            # Try Decimal conversion for other numeric-like types
            try:
                return self.format_string(str(Decimal(str(x))))
            except Exception:
                raise ValueError("Unsupported input type for format")

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        if not isinstance(x, str):
            raise ValueError("Input must be a string")

        s = x.strip().replace(",", "").replace("_", "")
        if not s:
            raise ValueError("Empty string")

        negative = False
        if s[0] in "+-":
            negative = s[0] == "-"
            s = s[1:]

        if not s:
            raise ValueError("Invalid number")

        # Validate numeric format (digits with optional single decimal point)
        if s.count(".") > 1:
            raise ValueError("Invalid number format")

        parts = s.split(".")
        int_part = parts[0] if parts[0] != "" else "0"
        if not int_part.isdigit():
            raise ValueError("Invalid integer part")

        dec_part = ""
        if len(parts) == 2:
            dec_part = parts[1]
            if dec_part and not dec_part.isdigit():
                raise ValueError("Invalid fractional part")

        int_words = self._format_integer_part(int_part)
        dec_words = self._format_decimal_part(dec_part)

        words = []
        if negative:
            words.append("MINUS")
        words.append(int_words if int_words else "ZERO")
        if dec_words:
            words.append("POINT")
            words.append(dec_words)

        return (" ".join(words) + " ONLY").replace("  ", " ").strip()

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        if not isinstance(s, str) or not s.isdigit() or not (1 <= len(s) <= 2):
            raise ValueError("trans_two expects a 1 or 2 digit numeric string")

        if len(s) == 1:
            n = int(s)
            return self.NUMBER[n] if n != 0 else ""

        a, b = int(s[0]), int(s[1])
        if a == 0:
            return self.NUMBER[b]
        if a == 1:
            return self.NUMBER_TEEN[b]
        if b == 0:
            return self.NUMBER_TEN[a - 1]
        return self.NUMBER_TEN[a - 1] + " " + self.NUMBER[b]

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        if not isinstance(s, str) or not s.isdigit() or not (1 <= len(s) <= 3):
            raise ValueError(
                "trans_three expects a 1 to 3 digit numeric string")

        s = s.zfill(3)
        h, t, u = int(s[0]), int(s[1]), int(s[2])
        parts = []

        if h != 0:
            parts.append(self.NUMBER[h] + " HUNDRED")
            if t != 0 or u != 0:
                parts.append("AND")

        two = self.trans_two(str(t) + str(u)) if (t != 0 or u != 0) else ""
        if two:
            parts.append(two)

        return " ".join(parts).strip()

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if not isinstance(i, int) or i < 0:
            return ""
        return self.NUMBER_MORE[i] if i < len(self.NUMBER_MORE) else ""

    def _format_integer_part(self, s):
        s = s.lstrip("0") or "0"
        if s == "0":
            return "ZERO"

        groups = []
        i = len(s)
        while i > 0:
            groups.append(s[max(0, i - 3):i])
            i -= 3

        words = []
        for idx, grp in enumerate(groups):
            w = self.trans_three(grp)
            if w:
                suffix = self.parse_more(idx)
                if suffix:
                    words.append(w + " " + suffix)
                else:
                    words.append(w)

        return " ".join(reversed(words)).strip()

    def _format_decimal_part(self, s):
        if s is None or s == "":
            return ""
        # Remove trailing zeros in fractional part? Keep as-is to reflect original number precisely.
        # If all zeros, return empty
        if all(ch == "0" for ch in s):
            return ""
        digit_words = ["ZERO", "ONE", "TWO", "THREE",
                       "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        return " ".join(digit_words[int(ch)] for ch in s)
