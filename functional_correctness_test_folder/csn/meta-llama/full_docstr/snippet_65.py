
from typing import Union, Iterable, List
from pythainlp.tokenize import word_tokenize
from pythainlp.util import Trie, dict_trie


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
        '''
        Initialize tokenizer object.
        :param str custom_dict: a file path, a list of vocaburaies* to be
                    used to create a trie, or an instantiated
                    :class:`pythainlp.util.Trie` object.
        :param str engine: choose between different options of tokenizer engines
                            (i.e.  *newmm*, *mm*, *longest*, *deepcut*)
        :param bool keep_whitespace: True to keep whitespace, a common mark
                                     for end of phrase in Thai
        '''
        self.__trie_dict = self.__load_dict(custom_dict)
        self.__engine = engine
        self.__keep_whitespace = keep_whitespace
        self.__join_broken_num = join_broken_num

    def __load_dict(self, custom_dict: Union[Trie, Iterable[str], str]) -> Trie:
        if isinstance(custom_dict, Trie):
            return custom_dict
        elif isinstance(custom_dict, str):
            with open(custom_dict, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f.readlines()]
            return dict_trie(words)
        else:
            return dict_trie(custom_dict)

    def word_tokenize(self, text: str) -> List[str]:
        '''
        Main tokenization function.
        :param str text: text to be tokenized
        :return: list of words, tokenized from the text
        :rtype: list[str]
        '''
        return word_tokenize(text, engine=self.__engine, custom_dict=self.__trie_dict,
                             keep_whitespace=self.__keep_whitespace, join_broken_num=self.__join_broken_num)

    def set_tokenizer_engine(self, engine: str) -> None:
        '''
        Set the tokenizer's engine.
        :param str engine: choose between different options of tokenizer engines
                           (i.e. *newmm*, *mm*, *longest*, *deepcut*)
        '''
        self.__engine = engine
