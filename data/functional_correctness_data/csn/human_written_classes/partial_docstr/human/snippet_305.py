import random
from pythainlp.corpus.oscar import unigram_word_freqs as oscar_word_freqs_unigram
from pythainlp.corpus.tnc import unigram_word_freqs as tnc_word_freqs_unigram
from pythainlp.corpus.ttc import unigram_word_freqs as ttc_word_freqs_unigram
from typing import List, Union

class Unigram:
    """
    Text generator using Unigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
        * *ttc* - Thai Textbook Corpus (TTC)
        * *oscar* - OSCAR Corpus
    """

    def __init__(self, name: str='tnc'):
        if name == 'tnc':
            self.counts = tnc_word_freqs_unigram()
        elif name == 'ttc':
            self.counts = ttc_word_freqs_unigram()
        elif name == 'oscar':
            self.counts = oscar_word_freqs_unigram()
        self.word = list(self.counts.keys())
        self.n = 0
        for i in self.word:
            self.n += self.counts[i]
        self.prob = {i: self.counts[i] / self.n for i in self.word}
        self._word_prob: dict = {}

    def gen_sentence(self, start_seq: str='', N: int=3, prob: float=0.001, output_str: bool=True, duplicate: bool=False) -> Union[List[str], str]:
        """
        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: List[str], str

        :Example:
        ::

            from pythainlp.generate import Unigram

            gen = Unigram()

            gen.gen_sentence("แมว")
            # output: 'แมวเวลานะนั้น'
        """
        if not start_seq:
            start_seq = random.choice(self.word)
        rand_text = start_seq.lower()
        self._word_prob = {i: self.counts[i] / self.n for i in self.word if self.counts[i] / self.n >= prob}
        return self._next_word(rand_text, N, output_str, prob=prob, duplicate=duplicate)

    def _next_word(self, text: str, N: int, output_str: bool, prob: float, duplicate: bool=False):
        words = []
        words.append(text)
        word_list = list(self._word_prob.keys())
        if N > len(word_list):
            N = len(word_list)
        for _ in range(N):
            w = random.choice(word_list)
            if duplicate is False:
                while w in words:
                    w = random.choice(word_list)
            words.append(w)
        if output_str:
            return ''.join(words)
        return words