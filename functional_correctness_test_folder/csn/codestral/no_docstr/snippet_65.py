
from typing import Union, Iterable, List
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
    :Example:
    Tokenizer object instantiated with :class:`pythainlp.util.Trie`::
        from pythainlp.tokenize import Tokenizer
        from pythainlp.corpus.common import thai_words
        from pythainlp.util import dict_trie
        custom_words_list = set(thai_words())
        custom_words_list.add('อะเฟเซีย')
        custom_words_list.add('Aphasia')
        trie = dict_trie(dict_source=custom_words_list)
        text = "อะเฟเซีย (Aphasia*) เป็นอาการผิดปกติของการพูด"
        _tokenizer = Tokenizer(custom_dict=trie, engine='newmm')
        _tokenizer.word_tokenize(text)
        # output: ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        'ผิดปกติ', 'ของ', 'การ', 'พูด']
    Tokenizer object instantiated with a list of words::
        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
        _tokenizer = Tokenizer(custom_dict=list(thai_words()), engine='newmm')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะ', 'เฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ',
        #   'ผิดปกติ', 'ของ', 'การ', 'พูด']
    Tokenizer object instantiated with a file path containing a list of
    words separated with *newline* and explicitly setting a new tokenizer
    after initiation::
        PATH_TO_CUSTOM_DICTIONARY = './custom_dictionary.txtt'
        # write a file
        with open(PATH_TO_CUSTOM_DICTIONARY, 'w', encoding='utf-8') as f:
            f.write('อะเฟเซีย\nAphasia\nผิด\nปกติ')
        text = "อะเฟเซีย (Aphasia) เป็นอาการผิดปกติของการพูด"
        # initiate an object from file with `attacut` as tokenizer
        _tokenizer = Tokenizer(custom_dict=PATH_TO_CUSTOM_DICTIONARY, \
            engine='attacut')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็น', 'อาการ', 'ผิด',
        #   'ปกติ', 'ของ', 'การ', 'พูด']
        # change tokenizer to `newmm`
        _tokenizer.set_tokenizer_engine(engine='newmm')
        _tokenizer.word_tokenize(text)
        # output:
        # ['อะเฟเซีย', ' ', '(', 'Aphasia', ')', ' ', 'เป็นอาการ', 'ผิด',
        #   'ปกติ', 'ของการพูด']
    '''

    def __init__(self, custom_dict: Union[Trie, Iterable[str], str] = [], engine: str = 'newmm', keep_whitespace: bool = True, join_broken_num: bool = True):

        self.custom_dict = custom_dict
        self.engine = engine
        self.keep_whitespace = keep_whitespace
        self.join_broken_num = join_broken_num

        if isinstance(self.custom_dict, str):
            with open(self.custom_dict, 'r', encoding='utf-8') as f:
                self.custom_dict = [line.strip() for line in f.readlines()]
        if isinstance(self.custom_dict, Iterable) and not isinstance(self.custom_dict, Trie):
            self.custom_dict = dict_trie(dict_source=self.custom_dict)

    def word_tokenize(self, text: str) -> List[str]:

        return word_tokenize(text, custom_dict=self.custom_dict, engine=self.engine, keep_whitespace=self.keep_whitespace, join_broken_num=self.join_broken_num)

    def set_tokenize_engine(self, engine: str) -> None:

        self.engine = engine
