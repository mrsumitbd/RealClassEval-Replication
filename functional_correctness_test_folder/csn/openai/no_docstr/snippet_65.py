
from typing import Union, Iterable, List
from pythainlp.tokenize import word_tokenize as _word_tokenize
from pythainlp.util import dict_trie, Trie


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
        join_broken_num: bool = True,
    ):
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num
        self.set_tokenize_engine(engine)

        # Resolve custom_dict to a Trie or None
        if isinstance(custom_dict, str):
            # Treat as file path
            try:
                with open(custom_dict, 'r', encoding='utf-8') as f:
                    words = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                raise ValueError(
                    f"Custom dictionary file not found: {custom_dict}")
            self.trie = dict_trie(dict_source=words)
        elif isinstance(custom_dict, Trie):
            self.trie = custom_dict
        elif isinstance(custom_dict, Iterable):
            # Convert iterable to set of strings
            words = set(str(w) for w in custom_dict)
            self.trie = dict_trie(dict_source=words) if words else None
        else:
            self.trie = None

    def word_tokenize(self, text: str) -> List[str]:
        """
        Tokenize the given text using the configured tokenizer engine and
        optional custom dictionary.
        """
        return _word_tokenize(
            text,
            engine=self.engine,
            custom_dict=self.trie,
            keep_whitespace=self.keep_whitespace,
            join_broken_num=self.join_broken_num,
        )

    def set_tokenize_engine(self, engine: str) -> None:
        """
        Set the tokenizer engine to use for subsequent tokenization.
        """
        if not isinstance(engine, str):
            raise TypeError("Engine must be a string")
        self.engine = engine
