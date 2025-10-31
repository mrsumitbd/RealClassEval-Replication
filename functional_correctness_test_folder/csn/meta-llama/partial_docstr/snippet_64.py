
from typing import List, Tuple
import fasttext
import random
from pythainlp.tokenize import word_tokenize


class FastTextAug:

    def __init__(self, model_path: str):
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        return word_tokenize(text, engine='newmm')

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        modified_sents = []
        for _ in range(len(tokens)):
            new_tokens = tokens.copy()
            if random.random() < p:
                similar_words = self.model.get_nearest_neighbors(
                    tokens[_], k=5)
                similar_words = [word for word, similarity in similar_words]
                if similar_words:
                    new_tokens[_] = random.choice(similar_words)
                    modified_sents.append(new_tokens)
        return modified_sents

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        modified_sents = self.modify_sent(sentence, p)
        if len(modified_sents) < n_sent:
            return [(' '.join(sent),) for sent in modified_sents]
        else:
            random_sents = random.sample(modified_sents, n_sent)
            return [(' '.join(sent),) for sent in random_sents]
