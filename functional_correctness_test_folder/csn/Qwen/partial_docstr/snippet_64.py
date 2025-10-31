
from typing import List, Tuple
import fasttext
import random


class FastTextAug:

    def __init__(self, model_path: str):
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        return self.model.get_words(text)

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        words = self.tokenize(sent)
        modified_words = []
        for word in words:
            if random.random() < p:
                similar_words = self.model.get_nearest_neighbors(word, k=5)
                if similar_words:
                    new_word = similar_words[random.randint(
                        0, len(similar_words) - 1)][1]
                    modified_words.append(new_word)
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        return [modified_words]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sentences = []
        for _ in range(n_sent):
            modified_words = self.modify_sent(sentence, p)[0]
            augmented_sentence = ' '.join(modified_words)
            augmented_sentences.append((augmented_sentence,))
        return augmented_sentences
