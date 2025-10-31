
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
        while center - diff >= 0 and center + diff < len(string) and string[center - diff] == string[center + diff]:
            diff += 1
        return diff - 1

    def palindromic_string(self):
        """
        Finds the longest palindromic substring in the given string.
        :return: The longest palindromic substring, str.
        >>> manacher = Manacher('ababaxse')
        >>> manacher.palindromic_string()
        'ababa'

        """
        modified_string = '|'.join(self.input_string)
        modified_string = '|' + modified_string + '|'
        max_length = 0
        max_center = 0
        right_boundary = 0
        right_boundary_center = 0
        p = [0] * len(modified_string)

        for i in range(len(modified_string)):
            if i < right_boundary:
                mirror = 2 * right_boundary_center - i
                p[i] = min(right_boundary - i, p[mirror])

            p[i] = self.palindromic_length(i, p[i] + 1, modified_string)

            if i + p[i] > right_boundary:
                right_boundary = i + p[i]
                right_boundary_center = i

            if p[i] > max_length:
                max_length = p[i]
                max_center = i

        start = (max_center - max_length) // 2
        end = start + max_length
        return self.input_string[start:end]
