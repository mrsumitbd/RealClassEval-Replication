
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
        for i, token in enumerate(tokens):
            if random.random() < p:
                neighbors = self.model.get_nearest_neighbors(token)
                if neighbors:
                    replacement = neighbors[0][1]
                    new_tokens = tokens.copy()
                    new_tokens[i] = replacement
                    modified_sentences.append(new_tokens)
        return modified_sentences

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sentences = []
        for _ in range(n_sent):
            modified = self.modify_sent(sentence, p)
            if modified:
                selected = random.choice(modified)
                augmented_sentences.append((' '.join(selected),))
            else:
                augmented_sentences.append((sentence,))
        return augmented_sentences
