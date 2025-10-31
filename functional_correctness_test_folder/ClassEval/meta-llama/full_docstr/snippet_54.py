
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
        'aM'
        """
        # Remove punctuation marks
        translator = str.maketrans('', '', string.punctuation)
        sentence_no_punct = sentence.translate(translator)

        # Split sentence into words
        words_in_sentence = sentence_no_punct.split()

        # Filter words that are in self.word_list
        valid_words = [
            word for word in words_in_sentence if word in self.word_list]

        # Return the longest valid word, or '' if self.word_list is empty or no valid words
        if not self.word_list or not valid_words:
            return ''
        else:
            return max(valid_words, key=len)
