from typing import List, Tuple, Optional
import os
import random
import re


class FastTextAug:
    '''
    Text Augment from fastText
    :param str model_path: path of model file
    '''

    def __init__(self, model_path: str):
        '''
        :param str model_path: path of model file
        '''
        if not isinstance(model_path, str) or not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self._backend = None
        self._model = None

        self._thai_re = re.compile(r'[\u0E00-\u0E7F]')
        self._word_re = re.compile(r'\w+', flags=re.UNICODE)

        # Try fasttext native model first (.bin/.ftz)
        try:
            import fasttext
            if model_path.endswith(('.bin', '.ftz')):
                self._model = fasttext.load_model(model_path)
                self._backend = 'fasttext'
        except Exception:
            pass

        # Fallback to gensim KeyedVectors (.vec, .txt)
        if self._model is None:
            try:
                from gensim.models import KeyedVectors
                binary = model_path.endswith('.bin') and self._backend is None
                self._model = KeyedVectors.load_word2vec_format(
                    model_path, binary=binary)
                self._backend = 'gensim'
            except Exception:
                pass

        if self._model is None or self._backend is None:
            raise RuntimeError(
                "Failed to load model. Ensure you have a valid fastText (.bin/.ftz) or word2vec (.vec/.txt) model and required libraries installed.")

        # Optional Thai tokenizer
        try:
            from pythainlp.tokenize import word_tokenize  # type: ignore
            self._thai_tokenize = lambda text: word_tokenize(
                text, engine="newmm")
        except Exception:
            self._thai_tokenize = None

        random.seed()

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        if not isinstance(text, str):
            return []
        has_thai = bool(self._thai_re.search(text))
        if has_thai and self._thai_tokenize is not None:
            toks = self._thai_tokenize(text)
            return [t for t in toks if t and not t.isspace()]
        # Generic Unicode tokenization fallback
        return self._word_re.findall(text)

    def _is_in_vocab(self, token: str) -> bool:
        if not token:
            return False
        try:
            if self._backend == 'fasttext':
                # fasttext returns vector for OOV via subwords but nearest neighbors may be poor;
                # We'll consider it in-vocab if word is known in its dict
                return token in self._model.get_words()
            else:
                return token in self._model.key_to_index  # gensim >=4
        except Exception:
            return False

    def _nearest(self, word: str, topn: int = 10) -> List[str]:
        res: List[str] = []
        try:
            if self._backend == 'fasttext':
                # returns list of (cosine, word)
                nn = self._model.get_nearest_neighbors(word, k=topn + 5)
                res = [w for _, w in nn if w != word]
            else:
                nn = self._model.most_similar(positive=[word], topn=topn + 5)
                res = [w for w, _ in nn if w != word]
        except Exception:
            res = []
        # Deduplicate, keep order
        seen = set()
        out = []
        for w in res:
            if w not in seen:
                seen.add(w)
                out.append(w)
            if len(out) >= topn:
                break
        return out

    def _should_join_without_space(self, original: str) -> bool:
        return bool(self._thai_re.search(original)) and (' ' not in original)

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        tokens = self.tokenize(sent)
        if not tokens:
            return [tokens]

        modified: List[str] = []
        for tok in tokens:
            cand = tok
            # Only attempt replacement for alphabetic Thai/word-like tokens
            if random.random() < max(0.0, min(1.0, p)) and self._is_in_vocab(tok):
                neighbors = self._nearest(tok, topn=8)
                if neighbors:
                    cand = random.choice(neighbors)
            modified.append(cand)
        return [modified]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        '''
        Text Augment from fastText
        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.
        :param str sentence: Thai sentence
        :param int n_sent: number of sentences
        :param float p: probability of word
        :return: list of synonyms
        :rtype: List[Tuple[str]]
        '''
        n_sent = max(1, int(n_sent))
        join_without_space = self._should_join_without_space(sentence)

        results: List[Tuple[str]] = []
        for _ in range(n_sent):
            mod_tok_lists = self.modify_sent(sentence, p=p)
            for toks in mod_tok_lists:
                if join_without_space:
                    aug = ''.join(toks)
                else:
                    aug = ' '.join(toks)
                results.append((aug,))
        return results
