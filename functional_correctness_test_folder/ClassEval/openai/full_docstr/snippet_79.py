
import re


class SplitSentence:
    """
    The class allows to split sentences, count words in a sentence, and process a text file to find the maximum word count.
    """

    def split_sentences(self, sentences_string):
        """
        Split a string into a list of sentences. Sentences end with . or ? and with a space after that.
        Please note that Mr. also end with . but are not sentences.
        :param sentences_string: string, string to split
        :return:list, split sentence list
        >>> ss = SplitSentence()
        >>> ss.split_sentences("aaa aaaa. bb bbbb bbb? cccc cccc. dd ddd?")
        ['aaa aaaa.', 'bb bbbb bbb?', 'cccc cccc.', 'dd ddd?']
        """
        sentences = []
        start = 0
        i = 0
        length = len(sentences_string)
        while i < length:
            ch = sentences_string[i]
            if ch in ".?":
                # check for Mr. pattern
                if i >= 2 and sentences_string[i-2:i+1] == "Mr.":
                    i += 1
                    continue
                # check that next char is space or end of string
                if i + 1 == length or sentences_string[i + 1] == " ":
                    sentence = sentences_string[start:i + 1].strip()
                    if sentence:
                        sentences.append(sentence)
                    start = i + 2  # skip the space after punctuation
                    i = start - 1
            i += 1
        return sentences

    def count_words(self, sentence):
        """
        Count the number of words in a sentence. Note that words are separated by spaces and that punctuation marks and numbers are not counted as words.
        :param sentence:string, sentence to be counted, where words are separated by spaces
        :return:int, number of words in the sentence
        >>> ss.count_words("abc def")
        2
        """
        # Find sequences of alphabetic characters
        words = re.findall(r'\b[A-Za-z]+\b', sentence)
        return len(words)

    def process_text_file(self, sentences_string):
        """
        Given a text, return the number of words in the longest sentence
        :param sentences_string: string, undivided long sentence
        :return:int, the number of words in the longest sentence
        >>> ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?")
        4
        """
        sentences = self.split_sentences(sentences_string)
        if not sentences:
            return 0
        max_words = max(self.count_words(s) for s in sentences)
        return max_words
