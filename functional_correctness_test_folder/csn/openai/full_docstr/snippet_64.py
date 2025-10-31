
import random
from typing import List, Tuple

import fasttext
from pythainlp.tokenize import word_tokenize


class FastTextAug:
    """
    Text Augment from fastText
    :param str model_path: path of model file
    """

    def __init__(self, model_path: str):
        """
        :param str model_path: path of model file
        """
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        """
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        """
        # Use the newmm engine for better Thai tokenization
        return word_tokenize(text, engine="newmm")

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        """
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        """
        words = self.tokenize(sent)
        modified = []

        for word in words:
            if random.random() < p:
                # Get nearest neighbors (synonyms) for the word
                neighbors = self.model.get_nearest_neighbors(word, k=10)
                # neighbors is a list of tuples (score, neighbor_word)
                if neighbors:
                    # Randomly pick one neighbor
                    _, syn = random.choice(neighbors)
                    modified.append(syn)
                else:
                    modified.append(word)
            else:
                modified.append(word)

        return [modified]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        """
        Text Augment from fastText
        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.
        :param str sentence: Thai sentence
        :param int n_sent: number of sentences
        :param float p: probability of word
        :return: list of synonyms
        :rtype: List[Tuple[str]]
        """
        augmented = []

        for _ in range(n_sent):
            variants = self.modify_sent(sentence, p)
            for variant in variants:
                augmented.append(("".join(variant),))

        return augmented
