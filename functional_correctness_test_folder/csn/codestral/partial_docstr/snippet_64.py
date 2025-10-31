
from typing import List, Tuple
import fasttext
import random


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
        words = self.model.get_words()
        tokens = []
        i = 0
        while i < len(text):
            for word in sorted(words, key=len, reverse=True):
                if text.startswith(word, i):
                    tokens.append(word)
                    i += len(word)
                    break
            else:
                tokens.append(text[i])
                i += 1
        return tokens

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        modified_tokens = []
        for token in tokens:
            if random.random() < p:
                neighbors = self.model.get_nearest_neighbors(token)
                if neighbors:
                    modified_token = random.choice(neighbors)[1]
                    modified_tokens.append(modified_token)
                else:
                    modified_tokens.append(token)
            else:
                modified_tokens.append(token)
        return [modified_tokens]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented_sentences = []
        for _ in range(n_sent):
            modified_tokens = self.modify_sent(sentence, p)
            augmented_sentence = ' '.join(modified_tokens[0])
            augmented_sentences.append((augmented_sentence,))
        return augmented_sentences
