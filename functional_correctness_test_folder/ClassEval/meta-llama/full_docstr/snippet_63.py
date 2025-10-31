
class NLPDataProcessor:
    """
    The class processes NLP data by removing stop words from a list of strings using a pre-defined stop word list.
    """

    def construct_stop_word_list(self):
        """
        Construct a stop word list including 'a', 'an', 'the'.
        :return: a list of stop words
        >>> NLPDataProcessor().construct_stop_word_list()
        ['a', 'an', 'the']
        """
        return ['a', 'an', 'the']

    def remove_stop_words(self, string_list, stop_word_list):
        """
        Remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :param stop_word_list: a list of stop words
        :return: a list of words without stop words
        >>> NLPDataProcessor().remove_stop_words(['This is a test.'], ['a'])
        [['This', 'is', 'test.']]
        """
        result = []
        for string in string_list:
            words = string.split()
            filtered_words = [
                word for word in words if word.lower() not in stop_word_list]
            result.append(filtered_words)
        return result

    def process(self, string_list):
        """
        Construct a stop word list including 'a', 'an', 'the', and remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :return: a list of words without stop words
        >>> NLPDataProcessor().process(['This is a test.'])
        [['This', 'is', 'test.']]
        """
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)


# Example usage:
if __name__ == "__main__":
    processor = NLPDataProcessor()
    print(processor.process(['This is a test.']))
    print(processor.remove_stop_words(['This is a test.'], ['a']))
    print(processor.construct_stop_word_list())
