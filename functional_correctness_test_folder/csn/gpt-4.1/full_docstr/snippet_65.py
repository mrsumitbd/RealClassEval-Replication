
from typing import Union, Iterable, List
from pythainlp.tokenize import word_tokenize as pythai_word_tokenize
from pythainlp.util import Trie, dict_trie


class Tokenizer:
    '''
    Tokenizer class for a custom tokenizer.
    This class allows users to pre-define custom dictionary along with
    tokenizer and encapsulate them into one single object.
    It is an wrapper for both functions, that are
    :func:`pythainlp.tokenize.word_tokenize`,
    and :func:`pythainlp.util.dict_trie`
    '''

    def __init__(
        self,
        custom_dict: Union[Trie, Iterable[str], str] = [],
        engine: str = 'newmm',
        keep_whitespace: bool = True,
        join_broken_num: bool = True
    ):
        self._engine = engine
        self._keep_whitespace = keep_whitespace
        self._join_broken_num = join_broken_num

        # Handle custom_dict
        if isinstance(custom_dict, Trie):
            self._custom_dict = custom_dict
        elif isinstance(custom_dict, str):
            # Assume it's a file path
            with open(custom_dict, encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
            self._custom_dict = dict_trie(words)
        elif isinstance(custom_dict, Iterable):
            # Could be list, set, tuple, etc.
            self._custom_dict = dict_trie(custom_dict)
        else:
            self._custom_dict = None

    def word_tokenize(self, text: str) -> List[str]:
        return pythai_word_tokenize(
            text,
            custom_dict=self._custom_dict,
            engine=self._engine,
            keep_whitespace=self._keep_whitespace,
            join_broken_num=self._join_broken_num
        )

    def set_tokenizer_engine(self, engine: str) -> None:
        self._engine = engine
