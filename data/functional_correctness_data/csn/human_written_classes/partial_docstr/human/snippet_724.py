from glyphsLib.types import IndexPath, Point, Rect, Transform, UnicodesList, floatToString5, parse_datetime, parse_float_or_int, readIntlist

class GSBase:
    """Represent the base class for all GS classes.

    Attributes:
        _defaultsForName (dict): Used to determine which values to serialize and which
            to imply by their absence.
    """
    _defaultsForName = {}

    def __repr__(self):
        content = ''
        if hasattr(self, '_dict'):
            content = str(self._dict)
        return f'<{self.__class__.__name__} {content}>'

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @classmethod
    def _add_parsers(cls, specification):
        for field in specification:
            keyname = field['plist_name']
            dict_parser_name = '_parse_%s_dict' % keyname
            target = field.get('object_name', keyname)
            classname = field.get('type')
            transformer = field.get('converter')

            def _generic_parser(self, parser, value, keyname=keyname, target=target, classname=classname, transformer=transformer):
                if transformer:
                    if isinstance(value, list) and transformer not in [IndexPath, Point, Rect]:
                        self[target] = [transformer(v) for v in value]
                    else:
                        self[target] = transformer(value)
                else:
                    obj = parser._parse(value, classname)
                    self[target] = obj
            setattr(cls, dict_parser_name, _generic_parser)