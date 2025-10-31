from typing import Iterable, List, Optional, Union


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

    def __init__(self, custom_dict: Union[Iterable[str], str] = [], engine: str = 'newmm', keep_whitespace: bool = True, join_broken_num: bool = True):
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
        self._engine = engine or 'newmm'
        self._keep_ws = bool(keep_whitespace)
        self._join_broken_num = bool(join_broken_num)
        self._dict: set[str] = set()
        self._max_word_len: int = 0
        self._load_dict(custom_dict)

    def _load_dict(self, custom_dict: Union[Iterable[str], str]) -> None:
        dict_words: set[str] = set()
        if isinstance(custom_dict, str):
            try:
                with open(custom_dict, 'r', encoding='utf-8') as f:
                    for line in f:
                        w = line.strip()
                        if w:
                            dict_words.add(w)
            except FileNotFoundError:
                pass
        else:
            try:
                # Some "Trie" implementations may be iterable over words
                for w in custom_dict:  # type: ignore
                    if isinstance(w, str) and w:
                        dict_words.add(w)
            except TypeError:
                pass

        self._dict = dict_words
        self._max_word_len = max((len(w) for w in self._dict), default=0)

    def _is_whitespace(self, ch: str) -> bool:
        return ch.isspace()

    def _is_punct(self, ch: str) -> bool:
        # Treat characters that are neither alnum nor mark nor underscore as punctuation
        # Keep underscore as word character
        if ch.isalnum() or ch == '_':
            return False
        # Unicode category starting with 'M' are marks (e.g., Thai combining marks)
        import unicodedata
        cat = unicodedata.category(ch)
        if cat.startswith('M'):
            return False
        return not self._is_whitespace(ch)

    def _is_word_char(self, ch: str) -> bool:
        if self._is_whitespace(ch):
            return False
        if ch.isalnum() or ch == '_':
            return True
        import unicodedata
        # Treat combining marks as part of word (for scripts like Thai)
        return unicodedata.category(ch).startswith('M')

    def _greedy_match_from(self, s: str, start: int) -> Optional[str]:
        if not self._dict or self._max_word_len <= 0:
            return None
        end_limit = min(len(s), start + self._max_word_len)
        best = None
        # Try longest first
        for end in range(end_limit, start, -1):
            cand = s[start:end]
            if cand in self._dict:
                best = cand
                break
        return best

    def _tokenize_word_run(self, run: str) -> List[str]:
        tokens: List[str] = []
        i = 0
        n = len(run)
        while i < n:
            # If number and join_broken_num, consume digits + [,.] inside
            if self._join_broken_num and run[i].isdigit():
                j = i + 1
                while j < n:
                    c = run[j]
                    if c.isdigit():
                        j += 1
                    elif c in '.,' and j + 1 < n and run[j + 1].isdigit():
                        j += 2
                    else:
                        break
                tokens.append(run[i:j])
                i = j
                continue

            # Try dictionary-based longest match
            m = self._greedy_match_from(run, i)
            if m:
                tokens.append(m)
                i += len(m)
                continue

            # If no dict match, consume contiguous alnum/mark as a unit until punctuation-like in run
            j = i + 1
            while j < n:
                c = run[j]
                if self._is_word_char(c):
                    j += 1
                else:
                    break
            tokens.append(run[i:j])
            i = j
        return tokens

    def word_tokenize(self, text: str) -> List[str]:
        '''
        Main tokenization function.
        :param str text: text to be tokenized
        :return: list of words, tokenized from the text
        :rtype: list[str]
        '''
        if not text:
            return []

        tokens: List[str] = []
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]

            if self._is_whitespace(ch):
                if self._keep_ws:
                    # Normalize any whitespace to single space tokens per character
                    tokens.append(' ')
                # Skip all consecutive whitespace characters
                i += 1
                while i < n and self._is_whitespace(text[i]):
                    if self._keep_ws:
                        tokens.append(' ')
                    i += 1
                continue

            if self._is_word_char(ch):
                # Collect a run of word characters
                j = i + 1
                while j < n and self._is_word_char(text[j]):
                    j += 1
                run = text[i:j]
                tokens.extend(self._tokenize_word_run(run))
                i = j
                continue

            if self._is_punct(ch):
                tokens.append(ch)
                i += 1
                continue

            # Fallback to single character
            tokens.append(ch)
            i += 1

        return tokens

    def set_tokenize_engine(self, engine: str) -> None:
        '''
        Set the tokenizer's engine.
        :param str engine: choose between different options of tokenizer engines
                           (i.e. *newmm*, *mm*, *longest*, *deepcut*)
        '''
        self._engine = engine or self._engine

    # Alias to match example usage
    def set_tokenizer_engine(self, engine: str) -> None:
        self.set_tokenize_engine(engine)
