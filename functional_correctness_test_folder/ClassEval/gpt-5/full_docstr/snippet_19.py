class CamelCaseMap:
    """
    This is a custom class that allows keys to be in camel case style by converting them from underscore style, which provides dictionary-like functionality.
    """

    def __init__(self):
        """
        Initialize data to an empty dictionary
        """
        self._data = {}

    def __getitem__(self, key):
        """
        Return the value corresponding to the key
        :param key:str
        :return:str,the value corresponding to the key
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map['first_name'] = 'John'
        >>> camelize_map.__getitem__('first_name')
        'John'
        """
        ckey = self._convert_key(key)
        return self._data[ckey]

    def __setitem__(self, key, value):
        """
        Set the value corresponding to the key to the specified value
        :param key:str
        :param value:str, the specified value
        :return:None
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map['first_name'] = 'John'
        >>> camelize_map.__setitem__('first_name', 'new name')
        camelize_map['first_name'] = 'new name'
        """
        ckey = self._convert_key(key)
        self._data[ckey] = value

    def __delitem__(self, key):
        """
        Delete the value corresponding to the key
        :param key:str
        :return:None
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map['first_name'] = 'John'
        >>> camelize_map.__delitem__('first_name')
        >>> flag = 'first_name' in camelize_map
        flag = False
        """
        ckey = self._convert_key(key)
        del self._data[ckey]

    def __iter__(self):
        """
        Returning Iterateable Objects with Own Data
        :return:Iterator
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map['first_name'] = 'John'
        >>> camelize_map['last_name'] = 'Doe'
        >>> camelize_map['age'] = 30
        >>> camelize_map.__iter__()
        <dict_keyiterator object at 0x0000026739977C20>
        """
        return iter(self._data.keys())

    def __len__(self):
        """
        Returns the length of the own data
        :return:int, length of data
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map['first_name'] = 'John'
        >>> camelize_map['last_name'] = 'Doe'
        >>> camelize_map['age'] = 30
        >>> camelize_map.__len__()
        3
        """
        return len(self._data)

    def __contains__(self, key):
        ckey = self._convert_key(key)
        return ckey in self._data

    def _convert_key(self, key):
        """
        convert key string into camel case
        :param key:str
        :return:str, converted key string
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map._convert_key('first_name')
        'firstName'
        """
        return self._to_camel_case(key)

    @staticmethod
    def _to_camel_case(key):
        """
        convert key string into camel case
        :param key:str
        :return:str, converted key string
        >>> camelize_map = CamelCaseMap()
        >>> camelize_map._to_camel_case('first_name')
        'firstName'
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not key:
            return key
        if "_" not in key:
            return key
        parts = [p for p in key.split("_") if p != ""]
        if not parts:
            return ""
        first = parts[0].lower()
        rest = []
        for p in parts[1:]:
            if not p:
                continue
            rest.append(p[:1].upper() + p[1:].lower())
        return first + "".join(rest)
