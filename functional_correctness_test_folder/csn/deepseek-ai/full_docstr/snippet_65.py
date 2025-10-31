
from typing import Union, List, Iterable
from pythainlp.tokenize import word_tokenize as pythai_word_tokenize
from pythainlp.util import dict_trie, Trie


class Tokenizer:
    def __init__(self, custom_dict: Union[Trie, Iterable[str], str] = None, engine: str = 'newmm', keep_whitespace: bool = True, join_broken_num: bool = True):
        self.engine = engine
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num
        self.custom_dict = custom_dict

        if isinstance(custom_dict, str):
            with open(custom_dict, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f.readlines()]
            self.trie = dict_trie(dict_source=words)
        elif isinstance(custom_dict, Trie):
            self.trie = custom_dict
        elif isinstance(custom_dict, Iterable):
            self.trie = dict_trie(dict_source=custom_dict)
        else:
            self.trie = None

    def word_tokenize(self, text: str) -> List[str]:
        return pythai_word_tokenize(
            text,
            custom_dict=self.trie,
            engine=self.engine,
            keep_whitespace=self.keep_whitespace,
            join_broken_num=self.join_broken_num
        )

    def set_tokenize_engine(self, engine: str) -> None:
        self.engine = engine
