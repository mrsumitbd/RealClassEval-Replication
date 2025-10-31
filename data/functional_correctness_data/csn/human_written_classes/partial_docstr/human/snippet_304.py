from typing import List, Union
from pythainlp.corpus.tnc import unigram_word_freqs as tnc_word_freqs_unigram
from pythainlp.corpus.tnc import bigram_word_freqs as tnc_word_freqs_bigram
from pythainlp.corpus.tnc import trigram_word_freqs as tnc_word_freqs_trigram
import random

class Trigram:
    """
    Text generator using Trigram

    :param str name: corpus name
        * *tnc* - Thai National Corpus (default)
    """

    def __init__(self, name: str='tnc'):
        if name == 'tnc':
            self.uni = tnc_word_freqs_unigram()
            self.bi = tnc_word_freqs_bigram()
            self.ti = tnc_word_freqs_trigram()
        self.uni_keys = list(self.uni.keys())
        self.bi_keys = list(self.bi.keys())
        self.ti_keys = list(self.ti.keys())
        self.words = [i[-1] for i in self.bi_keys]

    def prob(self, t1: str, t2: str, t3: str) -> float:
        """
        probability of word

        :param int t1: text 1
        :param int t2: text 2
        :param int t3: text 3

        :return: probability value
        :rtype: float
        """
        try:
            v = self.ti[t1, t2, t3] / self.bi[t1, t2]
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

            from pythainlp.generate import Trigram

            gen = Trigram()

            gen.gen_sentence()
            # output: 'ยังทำตัวเป็นเซิร์ฟเวอร์คือ'
        """
        if not start_seq:
            start_seq = random.choice(self.bi_keys)
        late_word = start_seq
        list_word = []
        list_word.append(start_seq)
        for i in range(N):
            if duplicate:
                temp = [j for j in self.ti_keys if j[:2] == late_word]
            else:
                temp = [j for j in self.ti_keys if j[:2] == late_word and j[1:] not in list_word]
            probs = [self.prob(word[0], word[1], word[2]) for word in temp]
            p2 = [j for j in probs if j >= prob]
            if len(p2) == 0:
                break
            items = temp[probs.index(random.choice(p2))]
            late_word = items[1:]
            list_word.append(late_word)
        listdata = []
        for i in list_word:
            for j in i:
                if j not in listdata:
                    listdata.append(j)
        if output_str:
            return ''.join(listdata)
        return listdata