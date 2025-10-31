
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
        modified_sents = []
        for _ in range(len(tokens)):
            new_tokens = tokens.copy()
            if random.random() < p:
                word = tokens[_]
                neighbors = self.model.get_nearest_neighbors(word, k=10)
                if neighbors:
                    new_word = random.choice([n[1] for n in neighbors])
                    new_tokens[_] = new_word
                    modified_sents.append(new_tokens)
        return modified_sents

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sentences = []
        for _ in range(n_sent):
            modified_sents = self.modify_sent(sentence, p)
            if modified_sents:
                augmented_sentences.append(
                    ' '.join(random.choice(modified_sents)))
            else:
                augmented_sentences.append(sentence)
        return list(set(augmented_sentences))
