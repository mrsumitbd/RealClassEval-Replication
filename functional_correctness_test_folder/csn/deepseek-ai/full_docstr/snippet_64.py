
from typing import List, Tuple
import fasttext
import fasttext.util
import numpy as np
from collections import defaultdict


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
        self.word_vectors = self.model.get_input_matrix()
        self.word_to_id = {word: i for i,
                           word in enumerate(self.model.get_words())}
        self.id_to_word = {i: word for i,
                           word in enumerate(self.model.get_words())}

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        return text.split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        words = self.tokenize(sent)
        modified_sentences = []
        for word in words:
            if word in self.word_to_id and np.random.random() < p:
                word_id = self.word_to_id[word]
                word_vec = self.word_vectors[word_id]
                similarities = np.dot(self.word_vectors, word_vec)
                # top 5 similar words
                similar_word_ids = np.argsort(-similarities)[1:6]
                similar_words = [self.id_to_word[id]
                                 for id in similar_word_ids]
                modified_sentences.append(similar_words)
            else:
                modified_sentences.append([word])
        return modified_sentences

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
        modified = self.modify_sent(sentence, p)
        augmented_sentences = []
        for _ in range(n_sent):
            new_sentence = []
            for choices in modified:
                new_sentence.append(np.random.choice(choices))
            augmented_sentences.append(tuple(new_sentence))
        return augmented_sentences
