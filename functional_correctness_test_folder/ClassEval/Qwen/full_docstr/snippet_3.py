
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
        import re
        args = re.findall(
            r'--?([a-zA-Z0-9_]+)(?:=([^\s]+))?|\s+([^\s]+)', command_string)
        for arg, value, value2 in args:
            if value2:
                arg, value = value, value2
            if value is None:
                value = True
            self.arguments[arg] = self._convert_type(arg, value)

        missing_args = self.required - self.arguments.keys()
        if missing_args:
            return False, missing_args
        return True, None

    def get_argument(self, key):
        """
        Retrieves the value of the specified argument from the arguments dictionary and returns it.
        """
        return self.arguments.get(key)

    def add_argument(self, arg, required=False, arg_type=str):
        """
        Adds an argument to self.types and self.required.
        Check if it is a required argument and store the argument type.
        If the argument is set as required, it wull be added to the required set.
        The argument type and name are stored in the types dictionary as key-value pairs.
        """
        self.types[arg] = arg_type
        if required:
            self.required.add(arg)

    def _convert_type(self, arg, value):
        """
        Try to convert the type of input value by searching in self.types.
        """
        arg_type = self.types.get(arg, str)
        try:
            if arg_type == bool:
                return value.lower() in ['true', '1', 't', 'y', 'yes']
            return arg_type(value)
        except (ValueError, TypeError):
            return value
