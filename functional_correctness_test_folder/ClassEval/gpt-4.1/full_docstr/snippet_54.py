
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
        # Remove punctuation
        trans = str.maketrans('', '', string.punctuation)
        clean_sentence = sentence.translate(trans)
        words = clean_sentence.split()
        # Find the longest word in both words and self.word_list
        candidates = [w for w in words if w in self.word_list]
        if not candidates:
            return ''
        # Return the longest, if tie, return the first one
        return max(candidates, key=len)
