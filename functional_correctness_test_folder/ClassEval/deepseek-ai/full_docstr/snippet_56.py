
class Manacher:
    """
    his is a class that implements a manacher algorithm to find the Longest palindromic substring in a given string.
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
        if (center - diff) >= 0 and (center + diff) < len(string) and string[center - diff] == string[center + diff]:
            return 1 + self.palindromic_length(center, diff + 1, string)
        else:
            return 0

    def palindromic_string(self):
        """
        Finds the longest palindromic substring in the given string.
        :return: The longest palindromic substring, str.
        >>> manacher = Manacher('ababaxse')
        >>> manacher.palindromic_string()
        'ababa'
        """
        max_length = 0
        new_string = '|' + '|'.join(self.input_string) + '|'
        palindromes = [0] * len(new_string)
        center = 0
        right = 0

        for i in range(len(new_string)):
            mirror = 2 * center - i
            if i < right:
                palindromes[i] = min(right - i, palindromes[mirror])
            length = self.palindromic_length(i, palindromes[i] + 1, new_string)
            palindromes[i] += length
            if i + palindromes[i] > right:
                center = i
                right = i + palindromes[i]
                if palindromes[i] > max_length:
                    max_length = palindromes[i]
                    start = (i - max_length) // 2
                    end = (i + max_length) // 2

        return self.input_string[start:end]
