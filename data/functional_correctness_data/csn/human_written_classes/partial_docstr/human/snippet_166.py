class PreProcessorRegex:
    """Regex-based substitution text pre-processor.

    Runs a series of regex substitutions (``re.sub``) from each ``regex`` of a
    :class:`gtts.tokenizer.core.RegexBuilder` with an extra ``repl``
    replacement parameter.

    Args:
        search_args (iterable): String element(s) to be each passed to
            ``search_func`` to create a regex pattern. Each element is
            ``re.escape``'d before being passed.
        search_func (callable): A 'template' function that should take a
            string and return a string. It should take an element of
            ``search_args`` and return a valid regex search pattern string.
        repl (string): The common replacement passed to the ``sub`` method for
            each ``regex``. Can be a raw string (the case of a regex
            backreference, for example)
        flags: ``re`` flag(s) to compile with each `regex`.

    Example:
        Add "!" after the words "lorem" or "ipsum", while ignoring case::

            >>> import re
            >>> words = ['lorem', 'ipsum']
            >>> pp = PreProcessorRegex(words,
            ...                        lambda x: "({})".format(x), r'\\\\1!',
            ...                        re.IGNORECASE)

        In this case, the regex is a group and the replacement uses its
        backreference ``\\\\1`` (as a raw string). Looking at ``pp`` we get the
        following list of search/replacement pairs::

            >>> print(pp)
            (re.compile('(lorem)', re.IGNORECASE), repl='\\1!'),
            (re.compile('(ipsum)', re.IGNORECASE), repl='\\1!')

        It can then be run on any string of text::

            >>> pp.run("LOREM ipSuM")
            "LOREM! ipSuM!"

    See :mod:`gtts.tokenizer.pre_processors` for more examples.

    """

    def __init__(self, search_args, search_func, repl, flags=0):
        self.repl = repl
        self.regexes = []
        for arg in search_args:
            rb = RegexBuilder([arg], search_func, flags)
            self.regexes.append(rb.regex)

    def run(self, text):
        """Run each regex substitution on ``text``.

        Args:
            text (string): the input text.

        Returns:
            string: text after all substitutions have been sequentially
            applied.

        """
        for regex in self.regexes:
            text = regex.sub(self.repl, text)
        return text

    def __repr__(self):
        subs_strs = []
        for r in self.regexes:
            subs_strs.append("({}, repl='{}')".format(r, self.repl))
        return ', '.join(subs_strs)