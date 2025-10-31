from typing import List, Tuple, Optional
import random
import warnings


class FastTextAug:

    def __init__(self, model_path: str):
        self.model = None
        self._use_gensim = False
        self._thai_tokenizer = None
        # Load tokenizer if available
        try:
            from pythainlp.tokenize import word_tokenize  # type: ignore
            self._thai_tokenizer = word_tokenize
        except Exception:
            self._thai_tokenizer = None
        # Load fastText model via gensim if available
        if model_path:
            try:
                from gensim.models import KeyedVectors  # type: ignore
                self._use_gensim = True
                # Try native load
                try:
                    self.model = KeyedVectors.load(model_path, mmap='r')
                except Exception:
                    # Try word2vec format
                    binary = model_path.lower().endswith('.bin')
                    self.model = KeyedVectors.load_word2vec_format(
                        model_path, binary=binary)
            except Exception as e:
                warnings.warn(
                    f"Could not load model at '{model_path}': {e}. Augmentation will be limited.")
                self.model = None
                self._use_gensim = False

        # Determine vocabulary accessor if model is loaded
        if self.model is not None and self._use_gensim:
            # Gensim 4.x uses key_to_index
            if hasattr(self.model, 'key_to_index'):
                self._in_vocab = lambda w: w in self.model.key_to_index
            else:
                self._in_vocab = lambda w: w in self.model.vocab
        else:
            self._in_vocab = lambda w: False

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        if not text:
            return []
        # Prefer Thai tokenizer if available
        if self._thai_tokenizer is not None:
            try:
                tokens = self._thai_tokenizer(text, engine='newmm')
                # Filter out pure whitespace tokens
                return [t for t in tokens if t and not t.isspace()]
            except Exception:
                pass
        # Fallback: if there are spaces, split on whitespace; else character-level
        if any(ch.isspace() for ch in text):
            toks = text.split()
            return [t for t in toks if t]
        # No whitespace: return characters as tokens (crude fallback for Thai)
        return [ch for ch in text if not ch.isspace()]

    def _get_similar(self, token: str, topn: int = 10) -> List[str]:
        if self.model is None or not self._use_gensim:
            return []
        if not self._in_vocab(token):
            return []
        try:
            sims = self.model.most_similar(token, topn=topn)
            # sims is list of tuples (word, score)
            candidates = [w for w, _ in sims if w != token]
            return candidates
        except Exception:
            return []

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        tokens = self.tokenize(sent)
        if not tokens:
            return []
        variants: List[List[str]] = []
        # Option 1: create variants by replacing each eligible token independently
        for idx, tok in enumerate(tokens):
            if random.random() <= max(0.0, min(1.0, p)):
                cands = self._get_similar(tok, topn=10)
                if cands:
                    rep = random.choice(cands)
                    new_tokens = list(tokens)
                    new_tokens[idx] = rep
                    variants.append(new_tokens)
        # If no single-replacement variants and we have a model, try one random multi replacement attempt
        if not variants and self.model is not None:
            new_tokens = list(tokens)
            changed = False
            for idx, tok in enumerate(tokens):
                if random.random() <= max(0.0, min(1.0, p)):
                    cands = self._get_similar(tok, topn=10)
                    if cands:
                        new_tokens[idx] = random.choice(cands)
                        changed = True
            if changed:
                variants.append(new_tokens)
        # Fallback: keep original tokens if nothing changed
        if not variants:
            variants.append(tokens)
        return variants

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        if n_sent <= 0:
            return []
        variants = self.modify_sent(sentence, p=p)
        if not variants:
            variants = [self.tokenize(sentence)]
        # Determine join rule: if original sentence contains spaces, join with space; else join without
        join_with_space = any(ch.isspace() for ch in sentence.strip())

        def detok(toks: List[str]) -> str:
            if join_with_space:
                return " ".join(toks)
            return "".join(toks)
        # Prepare outputs
        outputs: List[Tuple[str]] = []
        # Shuffle to get diversity
        random.shuffle(variants)
        # If we have fewer variants than requested, sample with replacement
        if len(variants) >= n_sent:
            chosen = variants[:n_sent]
        else:
            chosen = variants + [random.choice(variants)
                                 for _ in range(n_sent - len(variants))]
        for toks in chosen:
            outputs.append((detok(toks),))
        return outputs
