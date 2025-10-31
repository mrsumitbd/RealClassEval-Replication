import ford.utils

class NameSelector:
    """
    Object which tracks what names have been provided for different
    entities in Fortran code. It will provide an identifier which is
    guaranteed to be unique. This identifier can then me used as a
    filename for the documentation of that entity.
    """

    def __init__(self):
        self._items = {}
        self._counts = {}

    def get_name(self, item):
        """
        Return the name for this item registered with this NameSelector.
        If no name has previously been registered, then generate a new
        one.
        """
        if not isinstance(item, ford.sourceform.FortranBase):
            raise TypeError(f"'{item}' is not of a type derived from FortranBase")
        if item in self._items:
            return self._items[item]
        else:
            if item.get_dir() not in self._counts:
                self._counts[item.get_dir()] = {}
            if item.name in self._counts[item.get_dir()]:
                num = self._counts[item.get_dir()][item.name] + 1
            else:
                num = 1
            self._counts[item.get_dir()][item.name] = num
            name = item.name.lower()
            for symbol, replacement in {'<': 'lt', '>': 'gt', '/': 'SLASH', '*': 'ASTERISK'}.items():
                name = name.replace(symbol, replacement)
            if name == '':
                name = '__unnamed__'
            if num > 1:
                name = name + '~' + str(num)
            self._items[item] = name
            return name