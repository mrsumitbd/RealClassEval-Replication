
from typing import List, Tuple
import fasttext
import random


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
        return text.split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        words = self.tokenize(sent)
        modified_sentences = []
        for _ in range(len(words)):
            modified_words = []
            for word in words:
                if random.random() < p:
                    synonyms = self.get_synonyms(word)
                    if synonyms:
                        modified_words.append(random.choice(synonyms))
                    else:
                        modified_words.append(word)
                else:
                    modified_words.append(word)
            modified_sentences.append(modified_words)
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
        augmented_sentences = []
        for _ in range(n_sent):
            modified_sentences = self.modify_sent(sentence, p)
            for modified_sentence in modified_sentences:
                augmented_sentences.append((' '.join(modified_sentence),))
        return augmented_sentences

    def get_synonyms(self, word: str) -> List[str]:
        '''
        Get synonyms for a given word using the fastText model
        :param str word: word to find synonyms for
        :return: list of synonyms
        :rtype: List[str]
        '''
        nearest_words = self.model.get_nearest_neighbors(word)
        synonyms = [word for score, word in nearest_words if score > 0.5]
        return synonyms
