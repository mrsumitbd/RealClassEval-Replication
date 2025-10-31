import re

class PreProcessorSub:
    """Simple substitution text preprocessor.

    Performs string-for-string substitution from list a find/replace pairs.
    It abstracts :class:`gtts.tokenizer.core.PreProcessorRegex` with a default
    simple substitution regex.

    Args:
        sub_pairs (list): A list of tuples of the style
            ``(<search str>, <replace str>)``
        ignore_case (bool): Ignore case during search. Defaults to ``True``.

    Example:
        Replace all occurrences of "Mac" to "PC" and "Firefox" to "Chrome"::

            >>> sub_pairs = [('Mac', 'PC'), ('Firefox', 'Chrome')]
            >>> pp = PreProcessorSub(sub_pairs)

        Looking at the ``pp``, we get the following list of
        search (regex)/replacement pairs::

            >>> print(pp)
            (re.compile('Mac', re.IGNORECASE), repl='PC'),
            (re.compile('Firefox', re.IGNORECASE), repl='Chrome')

        It can then be run on any string of text::

            >>> pp.run("I use firefox on my mac")
            "I use Chrome on my PC"

    See :mod:`gtts.tokenizer.pre_processors` for more examples.

    """

    def __init__(self, sub_pairs, ignore_case=True):

        def search_func(x):
            return u'{}'.format(x)
        flags = re.I if ignore_case else 0
        self.pre_processors = []
        for sub_pair in sub_pairs:
            pattern, repl = sub_pair
            pp = PreProcessorRegex([pattern], search_func, repl, flags)
            self.pre_processors.append(pp)

    def run(self, text):
        """Run each substitution on ``text``.

        Args:
            text (string): the input text.

        Returns:
            string: text after all substitutions have been sequentially
            applied.

        """
        for pp in self.pre_processors:
            text = pp.run(text)
        return text

    def __repr__(self):
        return ', '.join([str(pp) for pp in self.pre_processors])