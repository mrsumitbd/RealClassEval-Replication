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
        if not sentences_string:
            return []

        s = sentences_string
        n = len(s)
        result = []
        buf = []

        i = 0
        while i < n:
            ch = s[i]
            buf.append(ch)

            is_eos = False
            if ch in ('.', '?'):
                # Check "Mr." exception (do not end sentence on "Mr.")
                if ch == '.':
                    # Look back exactly two chars for 'M''r' to form "Mr."
                    if i >= 2 and s[i - 2:i + 1] == "Mr.":
                        # Ensure it is a standalone title (start or preceded by space)
                        if i - 3 < 0 or s[i - 3].isspace():
                            is_eos = False
                        else:
                            is_eos = True
                    else:
                        is_eos = True
                else:
                    is_eos = True

                # Only consider as end-of-sentence if followed by space or end of string
                if is_eos:
                    next_is_space_or_end = (i + 1 >= n) or s[i + 1].isspace()
                    if not next_is_space_or_end:
                        is_eos = False

                if is_eos:
                    sentence = "".join(buf).rstrip()
                    if sentence:
                        result.append(sentence)
                    buf = []
                    # Consume exactly one following space if present
                    if i + 1 < n and s[i + 1].isspace():
                        i += 1  # skip the space
            i += 1

        # If any trailing buffer remains without terminal punctuation, ignore or append?
        # By spec, sentences end with . or ?, so we ignore trailing text without terminator.
        return result

    def count_words(self, sentence):
        """
        Count the number of words in a sentence. Note that words are separated by spaces and that punctuation marks and numbers are not counted as words.
        :param sentence:string, sentence to be counted, where words are separated by spaces
        :return:int, number of words in the sentence
        >>> ss.count_words("abc def")
        2
        """
        if not sentence:
            return 0

        # Split on whitespace and count tokens that are purely alphabetic after trimming punctuation at ends
        punct = set('.,;:!?\'"()[]{}<>')
        count = 0
        for tok in sentence.split():
            # Strip leading/trailing punctuation
            start = 0
            end = len(tok)
            while start < end and tok[start] in punct:
                start += 1
            while end > start and tok[end - 1] in punct:
                end -= 1
            core = tok[start:end]
            if core.isalpha():
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
        if not sentences:
            return 0
        return max(self.count_words(s) for s in sentences)
