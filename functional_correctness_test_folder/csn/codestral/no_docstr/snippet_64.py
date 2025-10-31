
import fasttext
from typing import List, Tuple
import random


class FastTextAug:

    def __init__(self, model_path: str):

        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:

        return text.split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:

        tokens = self.tokenize(sent)
        modified_sentences = []

        for i in range(len(tokens)):
            if random.random() < p:
                neighbors = self.model.get_nearest_neighbors(tokens[i])
                if neighbors:
                    tokens[i] = neighbors[0][1]
            modified_sentences.append(tokens.copy())

        return modified_sentences

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:

        augmented_sentences = []
        for _ in range(n_sent):
            modified_sentences = self.modify_sent(sentence, p)
            augmented_sentences.extend(
                [(' '.join(sent),) for sent in modified_sentences])

        return augmented_sentences
