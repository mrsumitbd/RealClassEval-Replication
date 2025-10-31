
from typing import List, Tuple
import fasttext
import random
import re


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
        # Simple whitespace and punctuation-based tokenizer for Thai
        # (for real use, consider PyThaiNLP or similar)
        tokens = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
        return tokens

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        new_sents = []
        for i, word in enumerate(tokens):
            if random.random() < p:
                # Get 5 nearest neighbors
                neighbors = self.model.get_nearest_neighbors(word)
                synonyms = [w for _, w in neighbors if w != word]
                if synonyms:
                    for syn in synonyms[:3]:  # up to 3 synonyms
                        new_tokens = tokens.copy()
                        new_tokens[i] = syn
                        new_sents.append(new_tokens)
        if not new_sents:
            new_sents.append(tokens)
        return new_sents

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        augmented = []
        tries = 0
        max_tries = n_sent * 10
        seen = set()
        while len(augmented) < n_sent and tries < max_tries:
            tries += 1
            mod_sents = self.modify_sent(sentence, p)
            for tokens in mod_sents:
                aug_sent = ''.join(tokens) if re.match(
                    r'^[\u0E00-\u0E7F]+$', ''.join(tokens)) else ' '.join(tokens)
                if aug_sent not in seen:
                    seen.add(aug_sent)
                    augmented.append((aug_sent,))
                if len(augmented) >= n_sent:
                    break
        return augmented
