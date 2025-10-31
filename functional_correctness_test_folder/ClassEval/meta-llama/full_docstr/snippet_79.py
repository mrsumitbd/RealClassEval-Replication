
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
        # Use regular expression to split the string into sentences
        # The pattern matches '. ' or '? ' and captures the punctuation mark
        sentences = re.split('([.?\u2026]) ', sentences_string)
        # Combine each sentence with its corresponding punctuation mark
        result = [sentences[i] + sentences[i+1]
                  for i in range(0, len(sentences)-1, 2)]
        # If the last character of the input string is not a punctuation mark followed by a space,
        # the last sentence will be in the last element of the sentences list
        if len(sentences) % 2 != 0:
            result.append(sentences[-1].strip())
        return result

    def count_words(self, sentence):
        """
        Count the number of words in a sentence. Note that words are separated by spaces and that punctuation marks and numbers are not counted as words.
        :param sentence:string, sentence to be counted, where words are separated by spaces
        :return:int, number of words in the sentence
        >>> ss.count_words("abc def")
        2
        """
        # Remove punctuation marks and numbers from the sentence
        cleaned_sentence = re.sub(r'[^\w\s]|[\d_]', '', sentence)
        # Split the sentence into words and count them
        return len(cleaned_sentence.split())

    def process_text_file(self, sentences_string):
        """
        Given a text, return the number of words in the longest sentence
        :param sentences_string: string, undivided long sentence
        :return:int, the number of words in the longest sentence
        >>> ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?")
        4
        """
        # Split the text into sentences
        sentences = self.split_sentences(sentences_string)
        # Count the words in each sentence and return the maximum count
        return max(self.count_words(sentence) for sentence in sentences)


# Example usage:
if __name__ == "__main__":
    ss = SplitSentence()
    print(ss.split_sentences("aaa aaaa. bb bbbb bbb? cccc cccc. dd ddd?"))
    print(ss.count_words("abc def"))
    print(ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?"))
