
import fasttext
import random
from typing import List, Tuple


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
        return self.model.tokenize(text)

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        words = self.tokenize(sent)
        new_words = words.copy()
        for i in range(len(words)):
            if random.uniform(0, 1) < p:
                synonyms = self.model.get_nearest_neighbors(words[i])
                if synonyms:
                    new_words[i] = synonyms[0][1]
        return [new_words]

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
        augmented_sentences = []
        for _ in range(n_sent):
            modified_sent = self.modify_sent(sentence, p)
            augmented_sentences.append(
                tuple(' '.join(words) for words in modified_sent))
        return augmented_sentences
