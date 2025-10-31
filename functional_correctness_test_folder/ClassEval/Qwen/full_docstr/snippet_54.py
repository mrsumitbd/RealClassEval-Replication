
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
        """
        if not self.word_list:
            return ''

        # Remove punctuation and split the sentence into words
        translator = str.maketrans('', '', string.punctuation)
        words = sentence.translate(translator).split()

        # Find the longest word in the sentence that is also in the word list
        longest_word = ''
        for word in words:
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word

        return longest_word
