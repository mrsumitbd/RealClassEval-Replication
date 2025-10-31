import re

class Tokenizer:
    """An extensible but simple generic rule-based tokenizer.

    A generic and simple string tokenizer that takes a list of functions
    (called `tokenizer cases`) returning ``regex`` objects and joins them by
    "|" (regex alternation 'or') to create a single regex to use with the
    standard ``regex.split()`` function.

    ``regex_funcs`` is a list of any function that can return a ``regex``
    (from ``re.compile()``) object, such as a
    :class:`gtts.tokenizer.core.RegexBuilder` instance (and its ``regex``
    attribute).

    See the :mod:`gtts.tokenizer.tokenizer_cases` module for examples.

    Args:
        regex_funcs (list): List of compiled ``regex`` objects. Each
            function's pattern will be joined into a single pattern and
            compiled.
        flags: ``re`` flag(s) to compile with the final regex. Defaults to
            ``re.IGNORECASE``

    Note:
        When the ``regex`` objects obtained from ``regex_funcs`` are joined,
        their individual ``re`` flags are ignored in favour of ``flags``.

    Raises:
        TypeError: When an element of ``regex_funcs`` is not a function, or
            a function that does not return a compiled ``regex`` object.

    Warning:
        Joined ``regex`` patterns can easily interfere with one another in
        unexpected ways. It is recommended that each tokenizer case operate
        on distinct or non-overlapping characters/sets of characters
        (For example, a tokenizer case for the period (".") should also
        handle not matching/cutting on decimals, instead of making that
        a separate tokenizer case).

    Example:
        A tokenizer with a two simple case (*Note: these are bad cases to
        tokenize on, this is simply a usage example*)::

            >>> import re, RegexBuilder
            >>>
            >>> def case1():
            ...     return re.compile("\\,")
            >>>
            >>> def case2():
            ...     return RegexBuilder('abc', lambda x: "{}\\.".format(x)).regex
            >>>
            >>> t = Tokenizer([case1, case2])

        Looking at ``case1().pattern``, we get::

            >>> print(case1().pattern)
            '\\\\,'

        Looking at ``case2().pattern``, we get::

            >>> print(case2().pattern)
            'a\\\\.|b\\\\.|c\\\\.'

        Finally, looking at ``t``, we get them combined::

            >>> print(t)
            're.compile('\\\\,|a\\\\.|b\\\\.|c\\\\.', re.IGNORECASE)
             from: [<function case1 at 0x10bbcdd08>, <function case2 at 0x10b5c5e18>]'

        It can then be run on any string of text::

            >>> t.run("Hello, my name is Linda a. Call me Lin, b. I'm your friend")
            ['Hello', ' my name is Linda ', ' Call me Lin', ' ', " I'm your friend"]

    """

    def __init__(self, regex_funcs, flags=re.IGNORECASE):
        self.regex_funcs = regex_funcs
        self.flags = flags
        try:
            self.total_regex = self._combine_regex()
        except (TypeError, AttributeError) as e:
            raise TypeError('Tokenizer() expects a list of functions returning regular expression objects (i.e. re.compile). ' + str(e))

    def _combine_regex(self):
        alts = []
        for func in self.regex_funcs:
            alts.append(func())
        pattern = '|'.join((alt.pattern for alt in alts))
        return re.compile(pattern, self.flags)

    def run(self, text):
        """Tokenize `text`.

        Args:
            text (string): the input text to tokenize.

        Returns:
            list: A list of strings (token) split according to the tokenizer cases.

        """
        return self.total_regex.split(text)

    def __repr__(self):
        return str(self.total_regex) + ' from: ' + str(self.regex_funcs)