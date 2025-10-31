
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
        left = center - diff
        right = center + diff
        if left < 0 or right >= len(string):
            return diff - 1
        if string[left] != string[right]:
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
        s = self.input_string
        if not s:
            return ""
        # Preprocess: insert '|' between characters to handle even/odd palindromes
        t = '|'.join(s)
        t = f'{t}'
        n = len(t)
        max_len = 0
        center_index = 0
        for i in range(n):
            length = self.palindromic_length(i, 1, t)
            if length > max_len:
                max_len = length
                center_index = i
        # Extract the palindrome from the processed string
        start = center_index - max_len
        end = center_index + max_len
        palindrome = t[start:end+1].replace('|', '')
        return palindrome
