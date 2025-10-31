
from typing import List, Tuple
import random
import numpy as np
from pythainlp.tokenize import word_tokenize


class FastTextAug:

    def __init__(self, model_path: str):
        from gensim.models import FastText
        self.model = FastText.load(model_path)

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        return word_tokenize(text)

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        modified_sentences = []

        for i in range(len(tokens)):
            if random.random() < p:
                similar_words = []
                try:
                    similar_words = [
                        word for word, _ in self.model.wv.most_similar(tokens[i], topn=5)]
                except KeyError:
                    pass

                if similar_words:
                    for word in similar_words:
                        new_tokens = tokens.copy()
                        new_tokens[i] = word
                        modified_sentences.append(new_tokens)

        return modified_sentences

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        modified_sentences = self.modify_sent(sentence, p)
        if not modified_sentences:
            return [tuple(self.tokenize(sentence)) for _ in range(n_sent)]

        sampled_indices = np.random.choice(len(modified_sentences), size=min(
            n_sent, len(modified_sentences)), replace=False)
        augmented = [tuple(modified_sentences[i]) for i in sampled_indices]

        if len(augmented) < n_sent:
            remaining = n_sent - len(augmented)
            augmented += [tuple(self.tokenize(sentence))
                          for _ in range(remaining)]

        return augmented
