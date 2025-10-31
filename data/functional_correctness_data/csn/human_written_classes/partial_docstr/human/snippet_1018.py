from typing import Any, Callable, Iterable, Literal, Mapping, Optional, Sequence, Union

class WinLex:

    @classmethod
    def quote_args(cls, args: Sequence[str]):
        if len(args) > 2 and ('CMD.EXE' in args[0].upper() or '%COMSPEC%' in args[0].upper()) and (args[1].upper() == '/K' or args[1].upper() == '/C') and any((' ' in arg for arg in args[2:])):
            args = [cls.ensure_pad(args[0], '"'), args[1], '"%s"' % ' '.join((cls.ensure_pad(arg, '"') for arg in args[2:]))]
        else:
            args = [cls.quote_string(arg) for arg in args]
        return args

    @classmethod
    def quote_string(cls, s: Sequence[str]):
        """
        quotes a string if necessary.
        """
        s = s.strip('"')
        if s[0] in ('-', ' '):
            return s
        if ' ' in s or '/' in s:
            return '"%s"' % s
        return s

    @classmethod
    def ensure_pad(cls, name: str, pad: str='_'):
        """

        Examples:
            >>> ensure_pad('conda')
            '_conda_'

        """
        if not name or name[0] == name[-1] == pad:
            return name
        else:
            return '%s%s%s' % (pad, name, pad)