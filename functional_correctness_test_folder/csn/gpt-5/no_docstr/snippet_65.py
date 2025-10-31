from typing import Iterable, List, Optional, Union

try:
    from pythainlp.tokenize import word_tokenize as thai_word_tokenize
    from pythainlp.util import dict_trie, Trie  # type: ignore
except Exception:
    thai_word_tokenize = None
    Trie = object  # fallback for type checking

    def dict_trie(dict_source: Iterable[str]):  # type: ignore
        class _SimpleTrie:
            def __init__(self, words: Iterable[str]):
                self.words = set(words)

            def __contains__(self, item: str) -> bool:
                return item in self.words

        return _SimpleTrie(dict_source)


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

    def __init__(
        self,
        custom_dict: Union["Trie", Iterable[str], str] = [],
        engine: str = 'newmm',
        keep_whitespace: bool = True,
        join_broken_num: bool = True
    ):
        self.engine: str = engine
        self.keep_whitespace: bool = keep_whitespace
        self.join_broken_num: bool = join_broken_num
        self._raw_dict_source: Optional[Union["Trie",
                                              Iterable[str], str]] = custom_dict
        self.custom_dict = self._prepare_custom_dict(custom_dict)

    def _prepare_custom_dict(self, custom_dict: Union["Trie", Iterable[str], str, None]):
        if custom_dict is None or custom_dict == []:
            return None
        # If already a Trie-like object
        try:
            if Trie is not object and isinstance(custom_dict, Trie):
                return custom_dict
        except Exception:
            pass

        # If path to file
        if isinstance(custom_dict, str):
            words: List[str] = []
            with open(custom_dict, 'r', encoding='utf-8') as f:
                for line in f:
                    w = line.strip()
                    if w:
                        words.append(w)
            return dict_trie(dict_source=words)

        # Iterable of strings
        try:
            # Try to iterate and build
            words_iter = list(custom_dict)  # type: ignore[arg-type]
            return dict_trie(dict_source=words_iter)
        except Exception:
            return None

    def word_tokenize(self, text: str) -> List[str]:
        if thai_word_tokenize is not None:
            return thai_word_tokenize(
                text,
                engine=self.engine,
                keep_whitespace=self.keep_whitespace,
                custom_dict=self.custom_dict,
                join_broken_num=self.join_broken_num,
            )
        # Fallback simple tokenizer if pythainlp is unavailable
        if not text:
            return []
        # If we have a simple dict trie fallback, extract set for matching
        dict_words = None
        if self.custom_dict is not None and hasattr(self.custom_dict, "words"):
            dict_words = getattr(self.custom_dict, "words", None)

        tokens: List[str] = []
        i = 0
        n = len(text)

        def is_space(ch: str) -> bool:
            return ch.isspace()

        while i < n:
            ch = text[i]
            if is_space(ch):
                if self.keep_whitespace:
                    j = i + 1
                    while j < n and is_space(text[j]):
                        j += 1
                    tokens.append(text[i:j])
                    i = j
                else:
                    i += 1
                continue

            if dict_words:
                # Longest match
                j = n
                matched = None
                while j > i:
                    seg = text[i:j]
                    if seg in dict_words:
                        matched = seg
                        break
                    j -= 1
                if matched:
                    tokens.append(matched)
                    i += len(matched)
                    continue

            # Default: single character token
            tokens.append(ch)
            i += 1

        return tokens

    def set_tokenize_engine(self, engine: str) -> None:
        self.engine = engine

    # Backward-compatible alias (as shown in the docstring example)
    def set_tokenizer_engine(self, engine: str) -> None:
        self.set_tokenize_engine(engine)
