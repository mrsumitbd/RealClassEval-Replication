class NLPDataProcessor:
    """
    The class processes NLP data by removing stop words from a list of strings using a pre-defined stop word list.
    """

    @staticmethod
    def construct_stop_word_list():
        """
        Construct a stop word list including 'a', 'an', 'the'.
        :return: a list of stop words
        >>> NLPDataProcessor.construct_stop_word_list()
        ['a', 'an', 'the']
        """
        return ['a', 'an', 'the']

    @staticmethod
    def remove_stop_words(string_list, stop_word_list):
        """
        Remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :param stop_word_list: a list of stop words
        :return: a list of words without stop words
        >>> NLPDataProcessor.process(['This is a test.'])
        [['This', 'is', 'test.']]
        """
        if not isinstance(string_list, list):
            raise TypeError("string_list must be a list of strings")
        if not isinstance(stop_word_list, list):
            raise TypeError("stop_word_list must be a list of strings")
        result = []
        stop_set = set(stop_word_list)
        for s in string_list:
            if not isinstance(s, str):
                raise TypeError("All items in string_list must be strings")
            words = s.split()
            filtered = [w for w in words if w not in stop_set]
            result.append(filtered)
        return result

    @staticmethod
    def process(string_list):
        """
        Construct a stop word list including 'a', 'an', 'the', and remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :return: a list of words without stop words
        >>> NLPDataProcessor.process(['This is a test.'])
        [['This', 'is', 'test.']]
        """
        stop_words = NLPDataProcessor.construct_stop_word_list()
        return NLPDataProcessor.remove_stop_words(string_list, stop_words)
