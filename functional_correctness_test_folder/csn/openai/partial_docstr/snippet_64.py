
import fasttext
from typing import List, Tuple

try:
    # Try to import a Thai tokenizer if available
    from pythainlp import word_tokenize
except ImportError:
    word_tokenize = None


class FastTextAug:
    """
    A simple augmentation class that uses a fastText model to replace words
    in a Thai sentence with their nearest neighbours in the embedding space.
    """

    def __init__(self, model_path: str):
        """
        Load a fastText model from the given path.

        :param model_path: Path to the fastText binary or text model file.
        """
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Thai text for fastText.

        :param text: Thai sentence.
        :return: List of tokens.
        """
        if word_tokenize:
            # Use the newmm engine for better Thai tokenization
            return word_tokenize(text, engine="newmm")
        # Fallback: simple whitespace split
        return text.split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        """
        Replace words in the sentence with their nearest neighbours with probability p.

        :param sent: Original sentence.
        :param p: Probability of replacing a word.
        :return: List containing a single list of modified tokens.
        """
        tokens = self.tokenize(sent)
        new_tokens = []

        for token in tokens:
            if token.strip() == "":
                new_tokens.append(token)
                continue

            # Decide whether to replace this token
            if p > 0 and random.random() < p:
                # fastText returns a list of tuples (word, similarity)
                neighbors = self.model.get_nearest_neighbors(token, k=1)
                if neighbors:
                    # Use the nearest neighbour word
                    new_token = neighbors[0][1]
                    new_tokens.append(new_token)
                    continue
            # Keep original token if not replaced
            new_tokens.append(token)

        return [new_tokens]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        """
        Generate n_sent augmented sentences from the original sentence.

        :param sentence: Original sentence.
        :param n_sent: Number of augmented sentences to generate.
        :param p: Probability of replacing a word.
        :return: List of tuples, each containing one augmented sentence.
        """
        augmented = []
        for _ in range(n_sent):
            modified_tokens_list = self.modify_sent(sentence, p)
            # modify_sent returns a list with one token list
            modified_tokens = modified_tokens_list[0]
            augmented_sentence = " ".join(modified_tokens)
            augmented.append((augmented_sentence,))
        return augmented
