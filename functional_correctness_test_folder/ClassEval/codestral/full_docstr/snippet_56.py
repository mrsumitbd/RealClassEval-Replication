
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
        if not self.input_string:
            return ""

        processed_string = '#' + '#'.join(self.input_string) + '#'
        n = len(processed_string)
        palindrome_lengths = [0] * n
        center = right = 0

        for i in range(n):
            if i < right:
                mirror = 2 * center - i
                palindrome_lengths[i] = min(
                    right - i, palindrome_lengths[mirror])

            left = i - (palindrome_lengths[i] + 1)
            right = i + (palindrome_lengths[i] + 1)

            while left >= 0 and right < n and processed_string[left] == processed_string[right]:
                palindrome_lengths[i] += 1
                left -= 1
                right += 1

            if i + palindrome_lengths[i] > right:
                center, right = i, i + palindrome_lengths[i]

        max_length = max(palindrome_lengths)
        center_index = palindrome_lengths.index(max_length)
        start = (center_index - max_length) // 2
        end = start + max_length

        return self.input_string[start:end]
