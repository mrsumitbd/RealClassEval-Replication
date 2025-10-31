from pythainlp.corpus.tnc import unigram_word_freqs as tnc_word_freqs_unigram
from pythainlp.corpus.tnc import bigram_word_freqs as tnc_word_freqs_bigram
from typing import List, Union
import random

class Bigram:
    """
    Text generator using Bigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    def __init__(self, name: str='tnc'):
        if name == 'tnc':
            self.uni = tnc_word_freqs_unigram()
            self.bi = tnc_word_freqs_bigram()
        self.uni_keys = list(self.uni.keys())
        self.bi_keys = list(self.bi.keys())
        self.words = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str) -> float:
        """
        probability of word

        :param int t1: text 1
        :param int t2: text 2

        :return: probability value
        :rtype: float
        """
        try:
            v = self.bi[t1, t2] / self.uni[t1]
        except ZeroDivisionError:
            v = 0.0
        return v

    def gen_sentence(self, start_seq: str='', N: int=4, prob: float=0.001, output_str: bool=True, duplicate: bool=False) -> Union[List[str], str]:
        """
        :param str start_seq: word to begin sentence with
        :param int N: number of words
        :param bool output_str: output as string
        :param bool duplicate: allow duplicate words in sentence

        :return: list of words or a word string
        :rtype: List[str], str

        :Example:
        ::

            from pythainlp.generate import Bigram

            gen = Bigram()

            gen.gen_sentence("แมว")
            # output: 'แมวไม่ได้รับเชื้อมัน'
        """
        if not start_seq:
            start_seq = random.choice(self.words)
        late_word = start_seq
        list_word = []
        list_word.append(start_seq)
        for _ in range(N):
            if duplicate:
                temp = [j for j in self.bi_keys if j[0] == late_word]
            else:
                temp = [j for j in self.bi_keys if j[0] == late_word and j[1] not in list_word]
            probs = [self.prob(late_word, next_word[-1]) for next_word in temp]
            p2 = [j for j in probs if j >= prob]
            if len(p2) == 0:
                break
            items = temp[probs.index(random.choice(p2))]
            late_word = items[-1]
            list_word.append(late_word)
        if output_str:
            return ''.join(list_word)
        return list_word