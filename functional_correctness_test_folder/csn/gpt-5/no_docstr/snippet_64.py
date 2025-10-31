from typing import List, Tuple, Optional
import os
import re
import random


class FastTextAug:

    def __init__(self, model_path: str):
        self.model_path = model_path
        self._fasttext_model = None
        self._gensim_model = None
        self._use_fasttext = False
        self._use_gensim = False

        # Try loading via fasttext first (for .bin models)
        try:
            import fasttext  # type: ignore
            if os.path.isfile(self.model_path):
                self._fasttext_model = fasttext.load_model(self.model_path)
                self._use_fasttext = True
        except Exception:
            self._fasttext_model = None
            self._use_fasttext = False

        # If fasttext failed, try gensim (for .vec or word2vec format)
        if not self._use_fasttext:
            try:
                from gensim.models import KeyedVectors  # type: ignore
                # Attempt binary=False first (common for .vec)
                try:
                    self._gensim_model = KeyedVectors.load_word2vec_format(
                        self.model_path, binary=False)
                    self._use_gensim = True
                except Exception:
                    # Try binary=True (word2vec bin)
                    self._gensim_model = KeyedVectors.load_word2vec_format(
                        self.model_path, binary=True)
                    self._use_gensim = True
            except Exception:
                self._gensim_model = None
                self._use_gensim = False

        self._word_re = re.compile(r"\w+|[^\w\s]", re.UNICODE)

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return self._word_re.findall(text)

    def _nearest(self, word: str, topn: int = 20) -> List[str]:
        candidates: List[str] = []
        if self._use_fasttext and self._fasttext_model is not None:
            try:
                # fasttext returns list of (sim, word)
                nn = self._fasttext_model.get_nearest_neighbors(
                    word, k=topn * 2)
                candidates = [w for _, w in nn if w.lower() != word.lower()]
            except Exception:
                candidates = []
        elif self._use_gensim and self._gensim_model is not None:
            try:
                nn = self._gensim_model.most_similar(word, topn=topn * 2)
                candidates = [w for w, _ in nn if w.lower() != word.lower()]
            except Exception:
                candidates = []
        return [w for w in candidates if w.isalpha()]

    def _maybe_replace(self, token: str, p: float) -> str:
        # Replace only alphabetic tokens
        if not token.isalpha():
            return token
        if random.random() > p:
            return token
        neighbors = self._nearest(token, topn=20)
        if not neighbors:
            return token
        # Prefer a neighbor different from token, keep casing similar
        choice = random.choice(neighbors)
        if token.isupper():
            return choice.upper()
        if token[0].isupper():
            return choice.capitalize()
        return choice

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        if not (self._use_fasttext or self._use_gensim):
            return [tokens[:]]
        modified = [self._maybe_replace(tok, p) for tok in tokens]
        return [modified]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        results: List[Tuple[str]] = []
        for _ in range(max(1, n_sent)):
            mod_tokens_list = self.modify_sent(sentence, p=p)
            if not mod_tokens_list:
                results.append((sentence,))
                continue
            mod_tokens = mod_tokens_list[0]
            # Simple detokenization: join with spaces and then fix space before punctuation
            text = " ".join(mod_tokens)
            text = re.sub(r"\s+([,.!?;:])", r"\1", text)
            results.append((text,))
        return results
