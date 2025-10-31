
from typing import List, Tuple
import fasttext
import random
import os


class FastTextAug:

    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        return text.strip().split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        augmented = []
        for i, token in enumerate(tokens):
            if random.random() < p:
                # Get 5 nearest neighbors, skip the first (itself)
                neighbors = self.model.get_nearest_neighbors(token)
                synonyms = [w for _, w in neighbors if w != token]
                if synonyms:
                    for syn in synonyms[:3]:  # up to 3 synonyms
                        new_tokens = tokens.copy()
                        new_tokens[i] = syn
                        augmented.append(new_tokens)
        if not augmented:
            augmented.append(tokens)
        return augmented

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sents = []
        tries = 0
        max_tries = n_sent * 10
        seen = set()
        while len(augmented_sents) < n_sent and tries < max_tries:
            tries += 1
            aug_lists = self.modify_sent(sentence, p)
            for aug_tokens in aug_lists:
                aug_sent = ' '.join(aug_tokens)
                if aug_sent != sentence and aug_sent not in seen:
                    augmented_sents.append((aug_sent,))
                    seen.add(aug_sent)
                if len(augmented_sents) >= n_sent:
                    break
        if not augmented_sents:
            augmented_sents.append((sentence,))
        return augmented_sents
