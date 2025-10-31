
from typing import Union, Iterable, List, Optional
from pythainlp.tokenize import word_tokenize
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
    _VALID_ENGINES = {'newmm', 'mm', 'longest', 'deepcut'}

    def __init__(
        self,
        custom_dict: Union[Trie, Iterable[str], str] = [],
        engine: str = 'newmm',
        keep_whitespace: bool = True,
        join_broken_num: bool = True,
    ):
        '''
        Initialize tokenizer object.
        :param custom_dict: a file path, a list of vocabularies to be
                            used to create a trie, or an instantiated
                            :class:`pythainlp.util.Trie` object.
        :param engine: choose between different options of tokenizer engines
                       (i.e.  *newmm*, *mm*, *longest*, *deepcut*)
        :param keep_whitespace: True to keep whitespace, a common mark
                                for end of phrase in Thai
        '''
        if engine not in self._VALID_ENGINES:
            raise ValueError(f"Unsupported engine '{engine}'. "
                             f"Valid options: {sorted(self._VALID_ENGINES)}")
        self.engine = engine
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num

        # Resolve custom_dict to a Trie or None
        if isinstance(custom_dict, Trie):
            self.custom_dict = custom_dict
        elif isinstance(custom_dict, str):
            # Treat as file path
            try:
                with open(custom_dict, 'r', encoding='utf-8') as f:
                    words = [line.strip() for line in f if line.strip()]
            except OSError as exc:
                raise ValueError(
                    f"Could not read custom dictionary file: {exc}") from exc
            self.custom_dict = dict_trie(dict_source=words)
        elif isinstance(custom_dict, Iterable):
            # Iterable of strings
            words = [w for w in custom_dict if isinstance(w, str) and w]
            self.custom_dict = dict_trie(dict_source=words) if words else None
        else:
            # Empty or unsupported type
            self.custom_dict = None

    def word_tokenize(self, text: str) -> List[str]:
        '''
        Tokenize the given text using the configured engine and custom dictionary.
        '''
        return word_tokenize(
            text,
            engine=self.engine,
            custom_dict=self.custom_dict,
            keep_whitespace=self.keep_whitespace,
            join_broken_num=self.join_broken_num,
        )

    def set_tokenize_engine(self, engine: str) -> None:
        '''
        Set the tokenizer's engine.
        :param engine: choose between different options of tokenizer engines
                       (i.e. *newmm*, *mm*, *longest*, *deepcut*)
        '''
        if engine not in self._VALID_ENGINES:
            raise ValueError(f"Unsupported engine '{engine}'. "
                             f"Valid options: {sorted(self._VALID_ENGINES)}")
        self.engine = engine
