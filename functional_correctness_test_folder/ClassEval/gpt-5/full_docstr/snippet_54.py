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
        if not isinstance(word, str):
            raise TypeError("word must be a string")
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
        if not isinstance(sentence, str):
            raise TypeError("sentence must be a string")

        import string

        translator = str.maketrans({ch: ' ' for ch in string.punctuation})
        cleaned = sentence.translate(translator)
        words = cleaned.split()

        longest = ''
        longest_len = 0
        for w in words:
            if w in self.word_list:
                if len(w) > longest_len:
                    longest = w
                    longest_len = len(w)
        return longest
