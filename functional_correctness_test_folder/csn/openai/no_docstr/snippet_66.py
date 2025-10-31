
class ArgumentProcessor:
    """
    A simple command‑line argument processor.

    Parameters
    ----------
    options : dict
        Mapping of option names to a dict with keys:
            - 'has_value' (bool): whether the option expects a value.
            - 'default'   (any): default value if the option is not supplied.
    arguments : list
        Ordered list of positional argument names.
    """

    def __init__(self, options, arguments):
        # Validate options structure
        if not isinstance(options, dict):
            raise TypeError("options must be a dict")
        for opt, cfg in options.items():
            if not isinstance(cfg, dict):
                raise TypeError(f"option config for '{opt}' must be a dict")
            if 'has_value' not in cfg:
                raise KeyError(
                    f"option config for '{opt}' missing 'has_value'")
            if not isinstance(cfg['has_value'], bool):
                raise TypeError(f"'has_value' for option '{opt}' must be bool")
            if 'default' not in cfg:
                cfg['default'] = None

        if not isinstance(arguments, list):
            raise TypeError("arguments must be a list")

        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        """
        Parse the provided argument list.

        Parameters
        ----------
        argument_list : list
            List of command‑line arguments (strings).

        Returns
        -------
        dict
            Dictionary with keys:
                - 'options': dict of parsed options.
                - 'arguments': dict of positional arguments.
        """
        if not isinstance(argument_list, list):
            raise TypeError("argument_list must be a list")

        parsed_options = {opt: cfg['default']
                          for opt, cfg in self.options.items()}
        parsed_args = {}
        arg_index = 0
        i = 0
        while i < len(argument_list):
            token = argument_list[i]
            if token.startswith("--"):
                # Long option
                if "=" in token:
                    opt_name, value = token[2:].split("=", 1)
                else:
                    opt_name = token[2:]
                    value = None
                if opt_name not in self.options:
                    raise ValueError(f"Unknown option '--{opt_name}'")
                cfg = self.options[opt_name]
                if cfg['has_value']:
                    if value is None:
                        if i + 1 >= len(argument_list):
                            raise ValueError(
                                f"Option '--{opt_name}' expects a value")
                        value = argument_list[i + 1]
                        i += 1
                    parsed_options[opt_name] = value
                else:
                    parsed_options[opt_name] = True
            elif token.startswith("-") and token != "-":
                # Short option(s)
                shorts = token[1:]
                for j, ch in enumerate(shorts):
                    opt_name = ch
                    if opt_name not in self.options:
                        raise ValueError(f"Unknown option '-{opt_name}'")
                    cfg = self.options[opt_name]
                    if cfg['has_value']:
                        if j < len(shorts) - 1:
                            # value is the rest of the token
                            value = shorts[j + 1:]
                            parsed_options[opt_name] = value
                            break
                        else:
                            if i + 1 >= len(argument_list):
                                raise ValueError(
                                    f"Option '-{opt_name}' expects a value")
                            value = argument_list[i + 1]
                            parsed_options[opt_name] = value
                            i += 1
                            break
                    else:
                        parsed_options[opt_name] = True
            else:
                # Positional argument
                if arg_index >= len(self.arguments):
                    raise ValueError(
                        f"Unexpected positional argument '{token}'")
                parsed_args[self.arguments[arg_index]] = token
                arg_index += 1
            i += 1

        # Fill missing positional arguments with None
        for idx in range(arg_index, len(self.arguments)):
            parsed_args[self.arguments[idx]] = None

        return {"options": parsed_options, "arguments": parsed_args}
