
from typing import Union, Iterable, List
from pythainlp.tokenize import word_tokenize
from pythainlp.util import dict_trie, Trie


class Tokenizer:
    def __init__(self, custom_dict: Union[Trie, Iterable[str], str] = [], engine: str = 'newmm', keep_whitespace: bool = True, join_broken_num: bool = True):
        if isinstance(custom_dict, Trie):
            self.custom_trie = custom_dict
        elif isinstance(custom_dict, str):
            with open(custom_dict, 'r', encoding='utf-8') as f:
                words = f.read().splitlines()
            self.custom_trie = dict_trie(dict_source=words)
        else:
            self.custom_trie = dict_trie(dict_source=custom_dict)

        self.engine = engine
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num

    def word_tokenize(self, text: str) -> List[str]:
        return word_tokenize(text, custom_dict=self.custom_trie, engine=self.engine, keep_whitespace=self.keep_whitespace, join_broken_num=self.join_broken_num)

    def set_tokenize_engine(self, engine: str) -> None:
        self.engine = engine
