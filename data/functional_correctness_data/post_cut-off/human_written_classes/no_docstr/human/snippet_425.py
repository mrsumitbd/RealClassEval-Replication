from pathlib import Path
import tiktoken
import torch
import numpy as np

class TiktokenTokenizer:

    def __init__(self, vocab_file: str):
        self.num_special_tokens = 1000
        vocab_size = DEFAULT_TIKTOKEN_MAX_VOCAB
        pattern = PATTERN_TIKTOKEN
        special_tokens = SPECIAL_TOKENS.copy()
        inner_vocab_size = vocab_size - self.num_special_tokens
        token2id = reload_mergeable_ranks(vocab_file, max_vocab=inner_vocab_size)
        self.tokenizer = tiktoken.Encoding(name=Path(vocab_file).parent.name, pat_str=pattern, mergeable_ranks=token2id, special_tokens={})
        self._bos_id = special_tokens.index('<s>')
        self._eos_id = special_tokens.index('</s>')

    def encode(self, text):
        tokens = self.tokenizer.encode(text)
        tokens = [t + self.num_special_tokens for t in tokens]
        return tokens

    def decode(self, tokens):
        adjusted_tokens = [t - self.num_special_tokens for t in tokens if t not in {self._bos_id, self._eos_id} and t >= self.num_special_tokens]
        if adjusted_tokens:
            return self.tokenizer.decode(adjusted_tokens)
        else:
            return ''

    def batch_decode(self, ids):
        if isinstance(ids, np.ndarray) or torch.is_tensor(ids):
            ids = ids.tolist()
        if isinstance(ids[0], list):
            ids = ids[0]
        return self.decode(ids)

    @property
    def pad_id(self):
        return self._eos_id

    @property
    def bos_token_id(self):
        return self._bos_id

    @property
    def eos_token_id(self):
        return self._eos_id