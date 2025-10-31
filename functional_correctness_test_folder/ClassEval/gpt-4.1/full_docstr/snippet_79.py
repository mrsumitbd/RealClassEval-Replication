
import re


class SplitSentence:
    """
    The class allows to split sentences, count words in a sentence, and process a text file to find the maximum word count.
    """

    def split_sentences(self, sentences_string):
        """
        Split a string into a list of sentences. Sentences end with . or ? and with a space after that. Please note that Mr. also end with . but are not sentences.
        :param sentences_string: string, string to split
        :return:list, split sentence list
        >>> ss = SplitSentence()
        >>> ss.split_sentences("aaa aaaa. bb bbbb bbb? cccc cccc. dd ddd?")
        ['aaa aaaa.', 'bb bbbb bbb?', 'cccc cccc.', 'dd ddd?']
        """
        # Regex: match . or ? followed by a space, but not if preceded by 'Mr'
        # We'll use a loop to split at the right places
        result = []
        pattern = re.compile(r'(Mr\.)|([.?\!]) ')
        start = 0
        i = 0
        while i < len(sentences_string):
            m = pattern.search(sentences_string, i)
            if not m:
                break
            if m.group(1):  # 'Mr.' match, skip
                i = m.end(1)
                continue
            else:
                # m.group(2) is . or ? or !
                end = m.end(2)
                result.append(sentences_string[start:end])
                start = m.end()
                i = m.end()
        # Add the last part if any
        if start < len(sentences_string):
            result.append(sentences_string[start:].strip())
        # Remove empty strings if any
        result = [s for s in result if s]
        return result

    def count_words(self, sentence):
        """
        Count the number of words in a sentence. Note that words are separated by spaces and that punctuation marks and numbers are not counted as words.
        :param sentence:string, sentence to be counted, where words are separated by spaces
        :return:int, number of words in the sentence
        >>> ss.count_words("abc def")
        2
        """
        # A word is a sequence of only letters (no numbers, no punctuation)
        words = sentence.split()
        count = 0
        for w in words:
            # Remove leading/trailing punctuation
            w_clean = w.strip('.,?!:;"\'()[]{}')
            if w_clean.isalpha():
                count += 1
        return count

    def process_text_file(self, sentences_string):
        """
        Given a text, return the number of words in the longest sentence
        :param sentences_string: string, undivided long sentence
        :return:int, the number of words in the longest sentence
        >>> ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?")
        4
        """
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for s in sentences:
            cnt = self.count_words(s)
            if cnt > max_count:
                max_count = cnt
        return max_count
