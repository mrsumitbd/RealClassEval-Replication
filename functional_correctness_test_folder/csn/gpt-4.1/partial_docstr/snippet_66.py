
class ArgumentProcessor:

    def __init__(self, options, arguments):
        """
        :param options: dict, e.g. {"-f": "file", "--file": "file"}
        :param arguments: dict, e.g. {"file": {"required": True, "default": None}}
        """
        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        result = {}
        used_args = set()
        i = 0
        n = len(argument_list)
        # Reverse map: option -> cleaned name
        option_to_clean = self.options

        while i < n:
            arg = argument_list[i]
            if arg in option_to_clean:
                clean_name = option_to_clean[arg]
                used_args.add(clean_name)
                # Check if next value exists and is not another option
                if i + 1 < n and not argument_list[i + 1].startswith('-'):
                    value = argument_list[i + 1]
                    i += 2
                else:
                    value = True  # flag option
                    i += 1
                result[clean_name] = value
            else:
                i += 1  # skip unknown args

        # Fill in defaults for missing arguments
        for clean_name, props in self.arguments.items():
            if clean_name not in result:
                if "default" in props and props["default"] is not None:
                    result[clean_name] = props["default"]
                elif props.get("required", False):
                    raise ValueError(
                        f"Missing required argument: {clean_name}")

        return result
