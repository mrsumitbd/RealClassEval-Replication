import re

class RegexBuilder:
    """Builds regex using arguments passed into a pattern template.

    Builds a regex object for which the pattern is made from an argument
    passed into a template. If more than one argument is passed (iterable),
    each pattern is joined by "|" (regex alternation 'or') to create a
    single pattern.

    Args:
        pattern_args (iterable): String element(s) to be each passed to
            ``pattern_func`` to create a regex pattern. Each element is
            ``re.escape``'d before being passed.
        pattern_func (callable): A 'template' function that should take a
            string and return a string. It should take an element of
            ``pattern_args`` and return a valid regex pattern group string.
        flags: ``re`` flag(s) to compile with the regex.

    Example:
        To create a simple regex that matches on the characters "a", "b",
        or "c", followed by a period::

            >>> rb = RegexBuilder('abc', lambda x: "{}\\.".format(x))

        Looking at ``rb.regex`` we get the following compiled regex::

            >>> print(rb.regex)
            'a\\.|b\\.|c\\.'

        The above is fairly simple, but this class can help in writing more
        complex repetitive regex, making them more readable and easier to
        create by using existing data structures.

    Example:
        To match the character following the words "lorem", "ipsum", "meili"
        or "koda"::

            >>> words = ['lorem', 'ipsum', 'meili', 'koda']
            >>> rb = RegexBuilder(words, lambda x: "(?<={}).".format(x))

        Looking at ``rb.regex`` we get the following compiled regex::

            >>> print(rb.regex)
            '(?<=lorem).|(?<=ipsum).|(?<=meili).|(?<=koda).'

    """

    def __init__(self, pattern_args, pattern_func, flags=0):
        self.pattern_args = pattern_args
        self.pattern_func = pattern_func
        self.flags = flags
        self.regex = self._compile()

    def _compile(self):
        alts = []
        for arg in self.pattern_args:
            arg = re.escape(arg)
            alt = self.pattern_func(arg)
            alts.append(alt)
        pattern = '|'.join(alts)
        return re.compile(pattern, self.flags)

    def __repr__(self):
        return str(self.regex)