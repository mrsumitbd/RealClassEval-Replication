import re
import regex

class REPattern:
    """ Container for re.SRE_Pattern object augmented with Irregular matching rules

    >>> pattern = REPattern('Aaron[ ]Swartz')
    >>> pattern.match('Aaron Swartz').group()
    'Aaron Swartz'
    >>> pattern.fullmatch('Aaron Swartz!!')
    >>> pattern.fullmatch('Aaron Swartz').group()
    'Aaron Swartz'
    >>> pattern.match('Aaron Swartz!!').group()
    'Aaron Swartz'
    """

    def __init__(self, pattern):
        self._compiled_pattern = re.compile(pattern)
        for name in dir(self._compiled_pattern):
            if name in ('__class__', '__init__', 'fullmatch') and getattr(self, name, None):
                continue
            attr = getattr(self._compiled_pattern, name)
            try:
                setattr(self, name, attr)
                log.debug('{}.{}.{} successfully "inherited" `_regex.Pattern.{}{}`'.format(__package__, __name__, self.__class__, name, '()' if callable(attr) else ''))
            except:
                log.warning('Unable to "inherit" `_regex.Pattern.{}{}`'.format(name, '()' if callable(attr) else ''))

    def fullmatch(self, *args, **kwargs):
        return regex.fullmatch(self._compiled_pattern.pattern, *args, **kwargs)