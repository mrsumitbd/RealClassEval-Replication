class UnicodeToLatexConversionRule:
    """
    Specify a rule how to convert unicode characters into LaTeX escapes.

    .. py:attribute:: rule_type

       One of :py:data:`RULE_DICT`, :py:data:`RULE_REGEX`, or
       :py:data:`RULE_CALLABLE`.

    .. py:attribute:: rule

       A specification of the rule itself.  The `rule` attribute is an object
       that depends on what `rule_type` is set to.  See below.

    .. py:attribute:: replacement_latex_protection

       If non-`None`, then the setting here will override any
       `replacement_latex_protection` set on
       :py:class:`UnicodeToLatexConversionRule` objects.  By default the value
       is `None`, and you can set a replacement_latex_protection globally for
       all rules on the :py:class:`UnicodeToLatexEncoder` object.

       The use of this attribute is mainly in case you have a fancy rule in
       which you already guarantee that whatever you output is valid LaTeX even
       if concatenated with the remainder of the string; in this case you can
       set `replacement_latex_protection='none'` to avoid unnecessary or
       unwanted braces around the generated code.

       .. versionadded:: 2.10

          The `replacement_latex_protection` attribute was introduced in
          `pylatexenc 2.10`.


    Constructor syntax::

        UnicodeToLatexConversionRule(RULE_XXX, <...>)
        UnicodeToLatexConversionRule(rule_type=RULE_XXX, rule=<...>)

        UnicodeToLatexConversionRule(..., replacement_latex_protection='none')

    Note that you can get some built-in rules via the
    :py:func:`get_builtin_conversion_rules()` function::

        conversion_rules = get_builtin_conversion_rules('defaults') # all defaults


    Rules types:

      - `RULE_DICT`: If `rule_type` is `RULE_DICT`, then `rule` should be a
        dictionary whose keys are integers representing unicode code points
        (e.g., `0x210F`), and whose values are corresponding replacement strings
        (e.g., ``r'\\hbar'``).  See :py:func:`get_builtin_uni2latex_dict()` for
        an example.

      - `RULE_REGEX`: If `rule_type` is `RULE_REGEX`, then `rule` should be an
        iterable of tuple pairs `(compiled_regular_expression,
        replacement_string)` where `compiled_regular_expression` was obtained
        with `re.compile(...)` and `replacement_string` is anything that can be
        specified as the second (`repl`) argument of `re.sub(...)`.  This can be
        a replacement string that includes escapes (like ``\\1, \\2, \\g<name>``)
        for captured sub-expressions or a callable that takes a match object as
        argument.

        .. note::

           The replacement string is parsed like the second argument to
           `re.sub()` and backslashes have a special meaning because they can
           refer to captured sub-expressions.  For a literal backslash, use two
           backslashes ``\\\\`` in raw strings, four backslashes in normal
           strings.

        Example::

          regex_conversion_rule = UnicodeToLatexConversionRule(
              rule_type=RULE_REGEX,
              rule=[
                  # protect acronyms of capital letters with braces,
                  # e.g.: ABC -> {ABC}
                  (re.compile(r'[A-Z]{2,}'), r'{\\1}'),
                  # Additional rules, e.g., "..." -> "\\ldots"
                  (re.compile(r'...'), r'\\\\ldots'), # note double \\\\
              ]
          )

      - `RULE_CALLABLE`: If `rule_type` is `RULE_CALLABLE`, then `rule` should
        be a callable that accepts two arguments, the unicode string and the
        position in the string (an integer).  The callable will be called with
        the original unicode string as argument and the position of the
        character that needs to be encoded.  If this rule can encode the given
        character at the given position, it should return a tuple
        `(consumed_length, replacement_string)` where `consumed_length` is the
        number of characters in the unicode string that `replacement_string`
        represents.  If the character(s) at the given position can't be encoded
        by this rule, the callable should return `None` to indicate that further
        rules should be attempted.

        If the callable accepts an additional argument called `u2lobj`, then the
        :py:class:`UnicodeToLatexEncoder` instance is provided to that argument.

        For example, the following callable should achieve the same effect as
        the previous example with regexes::

          def convert_stuff(s, pos):
              m = re.match(r'[A-Z]{2,}', s, pos)
              if m is not None:
                  return (m.end()-m.start(), '{'+m.group()+'}')
              if s.startswith('...', pos): # or  s[pos:pos+3] == '...'
                  return (3, r'\\ldots')
              return None


    .. versionadded:: 2.0

       This class was introduced in `pylatexenc 2.0`.
    """

    def __init__(self, rule_type, rule=None, replacement_latex_protection=None):
        self.rule_type = rule_type
        self.rule = rule
        self.replacement_latex_protection = replacement_latex_protection

    def __repr__(self):
        return '{}(rule_type={!r}, rule=<{}>, replacement_latex_protection={})'.format(self.__class__.__name__, self.rule_type, type(self.rule).__name__, repr(self.replacement_latex_protection))