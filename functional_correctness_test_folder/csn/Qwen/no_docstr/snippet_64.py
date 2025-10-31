
from typing import List, Tuple
import fasttext
import random


class FastTextAug:

    def __init__(self, model_path: str):
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        return text.split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        modified_sentences = []
        for _ in range(len(tokens)):
            modified_tokens = tokens[:]
            for i in range(len(modified_tokens)):
                if random.random() < p:
                    similar_words = self.model.get_nearest_neighbors(
                        modified_tokens[i])
                    if similar_words:
                        modified_tokens[i] = similar_words[0][1]
            modified_sentences.append(modified_tokens)
        return modified_sentences

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sentences = []
        for _ in range(n_sent):
            modified_sentences = self.modify_sent(sentence, p)
            for modified_sentence in modified_sentences:
                augmented_sentences.append((' '.join(modified_sentence),))
        return augmented_sentences
