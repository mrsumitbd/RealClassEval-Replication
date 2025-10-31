
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
        engine: str = "newmm",
        keep_whitespace: bool = True,
        join_broken_num: bool = True,
    ):
        """
        Initialize tokenizer object.
        :param str custom_dict: a file path, a list of vocaburaies* to be
                    used to create a trie, or an instantiated
                    :class:`pythainlp.util.Trie` object.
        :param str engine: choose between different options of tokenizer engines
                            (i.e.  *newmm*, *mm*, *longest*, *deepcut*)
        :param bool keep_whitespace: True to keep whitespace, a common mark
                                     for end of phrase in Thai
        """
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num
        self.set_tokenize_engine(engine)

        # Resolve custom_dict
        if isinstance(custom_dict, Trie):
            self.custom_dict = custom_dict
        elif isinstance(custom_dict, str):
            # Assume file path
            try:
                with open(custom_dict, encoding="utf-8") as f:
                    words = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                raise ValueError(
                    f"Custom dictionary file not found: {custom_dict}")
            self.custom_dict = dict_trie(dict_source=words)
        else:
            # Iterable of strings
            words = list(custom_dict)
            self.custom_dict = dict_trie(dict_source=words)

    def word_tokenize(self, text: str) -> List[str]:
        """
        Main tokenization function.
        :param str text: text to be tokenized
        :return: list of words, tokenized from the text
        :rtype: list[str]
        """
        return _word_tokenize(
            text,
            engine=self.engine,
            custom_dict=self.custom_dict,
            keep_whitespace=self.keep_whitespace,
            join_broken_num=self.join_broken_num,
        )

    def set_tokenize_engine(self, engine: str) -> None:
        """
        Set the tokenizer's engine.
        :param str engine: choose between different options of tokenizer engines
                           (i.e. *newmm*, *mm*, *longest*, *deepcut*)
        """
        valid_engines = {"newmm", "mm", "longest", "deepcut"}
        if engine not in valid_engines:
            raise ValueError(
                f"Unsupported engine '{engine}'. Valid options: {valid_engines}")
        self.engine = engine
