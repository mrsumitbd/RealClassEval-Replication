import re
from collections import Counter
from typing import List, Dict


class NLPDataProcessor2:
    """
    The class processes NLP data by extracting words from a list of strings, calculating the frequency of each word, and returning the top 5 most frequent words.
    """

    def process_data(self, string_list: List[str]) -> List[List[str]]:
        """
        keep only English letters and spaces in the string, then convert the string to lower case, and then split the string into a list of words.
        :param string_list: a list of strings
        :return: words_list: a list of words lists
        >>> NLPDataProcessor.process_data(['This is a test.'])
        [['this', 'is', 'a', 'test']]
        """
        if not string_list:
            return []
        words_list: List[List[str]] = []
        for s in string_list:
            if not isinstance(s, str):
                s = "" if s is None else str(s)
            cleaned = re.sub(r"[^A-Za-z ]+", " ", s)
            lowered = cleaned.lower()
            tokens = [w for w in lowered.split() if w]
            words_list.append(tokens)
        return words_list

    def calculate_word_frequency(self, words_list: List[List[str]]) -> Dict[str, int]:
        """
        Calculate the word frequency of each word in the list of words list, and sort the word frequency dictionary by value in descending order.
        :param words_list: a list of words lists
        :return: top 5 word frequency dictionary, a dictionary of word frequency, key is word, value is frequency
        >>> NLPDataProcessor.calculate_word_frequency([['this', 'is', 'a', 'test'], ['this', 'is', 'another', 'test']])
        {'this': 2, 'is': 2, 'test': 2, 'a': 1, 'another': 1}
        """
        if not words_list:
            return {}
        flat_words: List[str] = []
        for lst in words_list:
            if lst:
                flat_words.extend(lst)
        if not flat_words:
            return {}
        counts = Counter(flat_words)
        first_index = {}
        for idx, w in enumerate(flat_words):
            if w not in first_index:
                first_index[w] = idx
        sorted_words = sorted(
            counts.items(), key=lambda kv: (-kv[1], first_index[kv[0]]))
        top5 = sorted_words[:5]
        return {w: c for w, c in top5}

    def process(self, string_list: List[str]) -> Dict[str, int]:
        """
        keep only English letters and spaces in the string, then convert the string to lower case, and then split the string into a list of words. Calculate the word frequency of each word in the list of words list, and sort the word frequency dictionary by value in descending order.
        :param string_list: a list of strings
        :return: top 5 word frequency dictionary, a dictionary of word frequency, key is word, value is frequency
        >>> NLPDataProcessor.process(['This is a test.', 'This is another test.'])
        {'this': 2, 'is': 2, 'test': 2, 'a': 1, 'another': 1}
        """
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)
