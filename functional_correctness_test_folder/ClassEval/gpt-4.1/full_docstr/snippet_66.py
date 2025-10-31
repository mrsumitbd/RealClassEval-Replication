
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
        if isinstance(x, str):
            return self.format_string(x)
        if isinstance(x, float):
            s = str(x)
            if '.' in s:
                int_part, dec_part = s.split('.')
                int_part = int(int_part)
                dec_part = dec_part.rstrip('0')
                if not dec_part:
                    return self.format(int_part)
                int_words = self.format(int_part)
                dec_words = self._format_decimal(dec_part)
                return f"{int_words} POINT {dec_words} ONLY"
            else:
                return self.format(int(x))
        if isinstance(x, int):
            if x == 0:
                return "ZERO ONLY"
            s = str(x)
            res = []
            s = s.zfill(((len(s) + 2) // 3) * 3)
            n = len(s) // 3
            for i in range(n):
                part = s[i * 3:(i + 1) * 3]
                if int(part) != 0:
                    words = self.trans_three(part)
                    if self.parse_more(n - i - 1):
                        words += " " + self.parse_more(n - i - 1)
                    res.append(words)
            result = ' '.join(res)
            result = result.strip()
            if result:
                result += " ONLY"
            return result
        raise ValueError("Unsupported type for format")

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        x = x.strip()
        if not x:
            return "ZERO ONLY"
        if '.' in x:
            int_part, dec_part = x.split('.')
            int_part = int_part.lstrip('0') or '0'
            dec_part = dec_part.rstrip('0')
            if not dec_part:
                return self.format(int(int_part))
            int_words = self.format(int(int_part))
            dec_words = self._format_decimal(dec_part)
            return f"{int_words} POINT {dec_words} ONLY"
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
        s = s.zfill(2)
        a, b = int(s[0]), int(s[1])
        if a == 0:
            return self.NUMBER[b]
        elif a == 1:
            return self.NUMBER_TEEN[b]
        else:
            if b == 0:
                return self.NUMBER_TEN[a - 1]
            else:
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
        s = s.zfill(3)
        a, b, c = int(s[0]), int(s[1]), int(s[2])
        res = []
        if a != 0:
            res.append(self.NUMBER[a] + " HUNDRED")
            if b != 0 or c != 0:
                res.append("AND")
        if b == 0 and c == 0:
            pass
        elif b == 0:
            res.append(self.NUMBER[c])
        elif b == 1:
            res.append(self.NUMBER_TEEN[c])
        else:
            if c == 0:
                res.append(self.NUMBER_TEN[b - 1])
            else:
                res.append(self.NUMBER_TEN[b - 1] + " " + self.NUMBER[c])
        return ' '.join([w for w in res if w])

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if 0 <= i < len(self.NUMBER_MORE):
            return self.NUMBER_MORE[i]
        return ""

    def _format_decimal(self, dec_part):
        return ' '.join(self.NUMBER[int(d)] if d != '0' else "ZERO" for d in dec_part)
