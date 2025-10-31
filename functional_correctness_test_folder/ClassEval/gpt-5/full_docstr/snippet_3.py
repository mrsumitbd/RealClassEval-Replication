class ArgumentParser:
    """
    This is a class for parsing command line arguments to a dictionary.
    """

    def __init__(self):
        """
        Initialize the fields.
        self.arguments is a dict that stores the args in a command line
        self.requried is a set that stores the required arguments
        self.types is a dict that stores type of every arguments.
        >>> parser.arguments
        {'key1': 'value1', 'option1': True}
        >>> parser.required
        {'arg1'}
        >>> parser.types
        {'arg1': 'type1'}
        """
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        """
        Parses the given command line argument string and invoke _convert_type to stores the parsed result in specific type in the arguments dictionary.
        Checks for missing required arguments, if any, and returns False with the missing argument names, otherwise returns True.
        :param command_string: str, command line argument string, formatted like "python script.py --arg1=value1 -arg2 value2 --option1 -option2"
        :return tuple: (True, None) if parsing is successful, (False, missing_args) if parsing fails,
            where missing_args is a set of the missing argument names which are str.
        >>> parser.parse_arguments("python script.py --arg1=value1 -arg2 value2 --option1 -option2")
        (True, None)
        >>> parser.arguments
        {'arg1': 'value1', 'arg2': 'value2', 'option1': True, 'option2': True}
        """
        import shlex

        self.arguments = {}
        tokens = shlex.split(command_string)

        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.startswith('-'):
                # handle forms: --arg=value or -arg=value
                if '=' in tok:
                    flag, val = tok.split('=', 1)
                    name = flag.lstrip('-')
                    self.arguments[name] = self._convert_type(name, val)
                    i += 1
                    continue
                # handle flag possibly followed by a value
                name = tok.lstrip('-')
                next_val = None
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    next_val = tokens[i + 1]
                    self.arguments[name] = self._convert_type(name, next_val)
                    i += 2
                    continue
                else:
                    # boolean flag without explicit value
                    # if a type is declared and is not bool, leave as True anyway
                    self.arguments[name] = True
                    i += 1
                    continue
            else:
                # ignore non-flag tokens like "python", "script.py"
                i += 1

        missing = {arg for arg in self.required if arg not in self.arguments}
        if missing:
            return (False, missing)
        return (True, None)

    def get_argument(self, key):
        """
        Retrieves the value of the specified argument from the arguments dictionary and returns it.
        :param key: str, argument name
        :return: The value of the argument, or None if the argument does not exist.
        >>> parser.arguments
        {'arg1': 'value1', 'arg2': 'value2', 'option1': True, 'option2': True}
        >>> parser.get_argument('arg2')
        'value2'
        """
        return self.arguments.get(key)

    def add_argument(self, arg, required=False, arg_type=str):
        """
        Adds an argument to self.types and self.required.
        Check if it is a required argument and store the argument type.
        If the argument is set as required, it wull be added to the required set.
        The argument type and name are stored in the types dictionary as key-value pairs.
        :param arg: str, argument name
        :param required: bool, whether the argument is required, default is False
        :param arg_type:str, Argument type, default is str
        >>> parser.add_argument('arg1', True, 'int')
        >>> parser.required
        {'arg1'}
        >>> parser.types
        {'arg1': 'int'}
        """
        if required:
            self.required.add(arg)
        # Store as provided to satisfy examples; conversion will resolve at runtime
        self.types[arg] = arg_type

    def _convert_type(self, arg, value):
        """
        Try to convert the type of input value by searching in self.types.
        :param value: str, the input value in command line
        :return: return corresponding value in self.types if convert successfully, or the input value oherwise
        >>> parser.types
        {'arg1': int}
        >>> parser._convert_type('arg1', '21')
        21
        """
        t = self.types.get(arg, None)

        # Resolve string type names to actual types if needed
        type_map = {'int': int, 'float': float, 'str': str, 'bool': bool}
        if isinstance(t, str):
            t_resolved = type_map.get(t.lower(), None)
        else:
            t_resolved = t

        if t_resolved is None:
            return value

        try:
            if t_resolved is bool:
                # Handle common boolean string representations
                if isinstance(value, bool):
                    return value
                v = str(value).strip().lower()
                if v in ('1', 'true', 'yes', 'y', 'on'):
                    return True
                if v in ('0', 'false', 'no', 'n', 'off'):
                    return False
                # Fallback: any non-empty string becomes True
                return bool(value)
            # For other types, direct cast
            return t_resolved(value)
        except Exception:
            # On failure, return original value
            return value
