
class ArgumentParser:
    """
    This is a class for parsing command line arguments to a dictionary.
    """

    def __init__(self):
        """
        Initialize the fields.
        self.arguments is a dict that stores the args in a command line
        self.required is a set that stores the required arguments
        self.types is a dict that stores type of every arguments.
        """
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        """
        Parses the given command line argument string and invoke _convert_type to stores the parsed result in specific type in the arguments dictionary.
        Checks for missing required arguments, if any, and returns False with the missing argument names, otherwise returns True.
        """
        import shlex
        tokens = shlex.split(command_string)
        args = {}
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith('--'):
                if '=' in token:
                    key, value = token[2:].split('=', 1)
                    args[key] = self._convert_type(key, value)
                else:
                    key = token[2:]
                    # Check if next token is a value or another option
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        value = tokens[i + 1]
                        args[key] = self._convert_type(key, value)
                        i += 1
                    else:
                        args[key] = True
            elif token.startswith('-') and not token.startswith('--'):
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    value = tokens[i + 1]
                    args[key] = self._convert_type(key, value)
                    i += 1
                else:
                    args[key] = True
            i += 1
        self.arguments = args
        missing = set()
        for req in self.required:
            if req not in self.arguments:
                missing.add(req)
        if missing:
            return (False, missing)
        return (True, None)

    def get_argument(self, key):
        """
        Retrieves the value of the specified argument from the arguments dictionary and returns it.
        """
        return self.arguments.get(key, None)

    def add_argument(self, arg, required=False, arg_type=str):
        """
        Adds an argument to self.types and self.required.
        """
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def _convert_type(self, arg, value):
        """
        Try to convert the type of input value by searching in self.types.
        """
        typ = self.types.get(arg, str)
        # If typ is a string, convert to type object
        if isinstance(typ, str):
            if typ == 'int':
                typ = int
            elif typ == 'float':
                typ = float
            elif typ == 'bool':
                def typ(v): return v.lower() in ('true', '1', 'yes', 'on')
            elif typ == 'str':
                typ = str
            else:
                typ = str
        try:
            return typ(value)
        except Exception:
            return value
