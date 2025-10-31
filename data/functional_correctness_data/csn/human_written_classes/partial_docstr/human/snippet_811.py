from textwrap import fill, indent

class OcrdEnvVariable:

    def __init__(self, name, description, parser=str, validator=lambda _: True, default=[False, None]):
        """
        An environment variable for use in OCR-D.

        Args:
            name (str): Name of the environment variable
            description (str): Description of what the variable is used for.

        Keyword Args:
            parser (callable): Function to transform the raw (string) value to whatever is needed.
            validator (callable): Function to validate that the raw (string) value is parseable.
            default (tuple(bool, any)): 2-tuple, first element is a bool whether there is a default
                value defined and second element contains that default value, which can be a callable
                for deferred evaluation
        """
        self.name = name
        self.description = description
        self.parser = parser
        self.validator = validator
        self.has_default = default[0]
        self.default = default[1]

    def __str__(self):
        return f'{self.name}: {self.description}'

    def describe(self, wrap_text=True, indent_text=True):
        """
        Output help information on a config option.

        If ``option.description`` is a multiline string with complex formatting
        (e.g. markdown lists), replace empty lines with ``\x08`` and set
        ``wrap_text`` to ``False``.
        """
        desc = self.description
        if self.has_default:
            default = self.default() if callable(self.default) else self.default
            if not desc.endswith('\n'):
                desc += ' '
            desc += f'(Default: "{default}")'
        ret = ''
        ret = f'{self.name}\n'
        if wrap_text:
            desc = fill(desc, width=50)
        if indent_text:
            ret = f'  {ret}'
            desc = indent(desc, '    ')
        return ret + desc