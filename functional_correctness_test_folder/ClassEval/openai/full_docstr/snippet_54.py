
import re
import string


class LongestWord:
    """
    This is a class allows to add words to a list and find the longest word in a given sentence by comparing the words with the ones in the word list.
    """

    def __init__(self):
        """
        Initialize a list of word.
        """
        self.word_list = []

    def add_word(self, word):
        """
        append the input word into self.word_list
        :param word: str, input word
        """
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        """
        Remove punctuation marks and split a sentence into a list of word. Find the longest splited word that is in the self.word_list.
        Words are strictly case sensitive.
        :param sentence: a sentence str
        :return str: longest splited word that is in the self.word_list. return '' if self.word_list is empty.
        >>> longestWord = LongestWord()
        >>> longestWord.add_word('A')
        >>> longestWord.add_word('aM')
        >>> longestWord.find_longest_word('I am a student.')
        'a'
        """
        if not self.word_list:
            return ''

        # Remove punctuation by replacing each punctuation character with a space
        # This keeps word boundaries intact
        translator = str.maketrans(
            string.punctuation, ' ' * len(string.punctuation))
        cleaned = sentence.translate(translator)

        # Split on whitespace
        words = cleaned.split()

        longest = ''
        for w in words:
            if w in self.word_list:
                if len(w) > len(longest):
                    longest = w
        return longest
