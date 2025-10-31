
from typing import List, Tuple
import fasttext
import numpy as np
import random
import pythainlp.tokenize


class FastTextAug:
    '''
    Text Augment from fastText
    :param str model_path: path of model file
    '''

    def __init__(self, model_path: str):
        '''
        :param str model_path: path of model file
        '''
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        return pythainlp.tokenize.word_tokenize(text)

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        words = self.tokenize(sent)
        new_sentences = []
        for _ in range(len(words)):
            new_words = words.copy()
            if random.random() < p:
                word = random.choice(words)
                neighbors = self.model.get_nearest_neighbors(word, k=5)
                if neighbors:
                    new_word = random.choice([n[1] for n in neighbors])
                    new_words = [new_word if w ==
                                 word else w for w in new_words]
            new_sentences.append(new_words)
        return new_sentences

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        '''
        Text Augment from fastText
        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.
        :param str sentence: Thai sentence
        :param int n_sent: number of sentences
        :param float p: probability of word
        :return: list of synonyms
        :rtype: List[Tuple[str]]
        '''
        new_sentences = []
        for _ in range(n_sent):
            modified_sentences = self.modify_sent(sentence, p)
            for modified_sentence in modified_sentences:
                new_sentence = ' '.join(modified_sentence)
                new_sentences.append(
                    tuple(pythainlp.tokenize.word_tokenize(new_sentence)))
        return list(set(new_sentences))
