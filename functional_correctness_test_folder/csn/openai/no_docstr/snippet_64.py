
import re
import random
from typing import List, Tuple

try:
    import fasttext
except ImportError:
    fasttext = None


class FastTextAug:
    """
    Simple FastText based data augmentation.
    """

    def __init__(self, model_path: str):
        """
        Load a FastText model from the given path.
        """
        if fasttext is None:
            raise ImportError("fasttext library is required for FastTextAug")
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into words and punctuation.
        """
        # Split on word boundaries and keep punctuation as separate tokens
        return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

    def _is_word(self, token: str) -> bool:
        """
        Check if a token is a word (contains alphabetic characters).
        """
        return bool(re.search(r"[A-Za-z]", token))

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        """
        Replace words in the sentence with synonyms with probability `p`.
        Returns a list containing a single modified token list.
        """
        tokens = self.tokenize(sent)
        new_tokens = []

        for token in tokens:
            if self._is_word(token):
                if random.random() < p:
                    # Get nearest neighbors (score, word)
                    neighbors = self.model.get_nearest_neighbors(token, k=10)
                    # Filter out the original word and non-alphabetic tokens
                    candidates = [
                        w for score, w in neighbors
                        if w.lower() != token.lower() and self._is_word(w)
                    ]
                    if candidates:
                        new_token = random.choice(candidates)
                        new_tokens.append(new_token)
                        continue
            new_tokens.append(token)

        return [new_tokens]

    def _detokenize(self, tokens: List[str]) -> str:
        """
        Join tokens into a string, handling spacing around punctuation.
        """
        text = " ".join(tokens)
        # Remove space before punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        return text

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        """
        Generate `n_sent` augmented sentences from the input `sentence`.
        Each augmentation is returned as a single-element tuple.
        """
        augmented = []
        for _ in range(n_sent):
            modified_lists = self.modify_sent(sentence, p)
            # We only generate one modification per call
            tokens = modified_lists[0]
            aug_sentence = self._detokenize(tokens)
            augmented.append((aug_sentence,))
        return augmented
