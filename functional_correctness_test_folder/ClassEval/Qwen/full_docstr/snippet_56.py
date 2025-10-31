
class Manacher:
    """
    This is a class that implements a manacher algorithm to find the Longest palindromic substring in a given string.
    """

    def __init__(self, input_string) -> None:
        """
        Initializes the Manacher class with the given input_string.
        :param input_string: The input_string to be searched, str.
        """
        self.input_string = input_string

    def palindromic_length(self, center, diff, string):
        """
        Recursively calculates the length of the palindromic substring based on a given center, difference value, and input string.
        :param center: The center of the palindromic substring, int.
        :param diff: The difference between the center and the current position, int.
        :param string: The string to be searched, str.
        :return: The length of the palindromic substring, int.
        >>> manacher = Manacher('ababa')
        >>> manacher.palindromic_length(2, 1, 'a|b|a|b|a')
        2

        """
        if center - diff < 0 or center + diff >= len(string) or string[center - diff] != string[center + diff]:
            return diff - 1
        return self.palindromic_length(center, diff + 1, string)

    def palindromic_string(self):
        """
        Finds the longest palindromic substring in the given string.
        :return: The longest palindromic substring, str.
        >>> manacher = Manacher('ababaxse')
        >>> manacher.palindromic_string()
        'ababa'

        """
        transformed_string = '|'.join(f'^{self.input_string}$')
        n = len(transformed_string)
        p = [0] * n
        center = right = 0
        max_len = max_center = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                p[i] = min(right - i, p[mirror])

            while transformed_string[i + p[i] + 1] == transformed_string[i - p[i] - 1]:
                p[i] += 1

            if i + p[i] > right:
                center, right = i, i + p[i]

            if p[i] > max_len:
                max_len, max_center = p[i], i

        start = (max_center - max_len) // 2
        return self.input_string[start:start + max_len]
