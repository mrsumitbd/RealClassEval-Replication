class ArgumentProcessor:
    def __init__(self, options, arguments):
        """
        options: dict or list
          - If dict: {
                "name": {
                    "aliases": ["-n", "--name"],
                    "type": callable (default str),
                    "default": any,
                    "required": bool (default False),
                    "action": "store", "store_true", "store_false", "count", "append",
                    "choices": iterable
                },
                ...
            }
          - If list: ["flag1", "flag2"] -> treated as boolean flags (store_true)
        arguments: list defining positional arguments
          Accepts:
            - ["arg1", "arg2"]
            - [("arg1", default), ("arg2", default)]
            - [{"name": "arg", "default": ..., "required": True, "multiple": True}, ...]
        """
        self.options_raw = options
        self.arguments_raw = arguments

        self.options = {}
        if isinstance(options, dict):
            for name, conf in options.items():
                self.options[self._clean_name(name)] = self._normalize_option_conf(
                    name, conf or {})
        elif isinstance(options, (list, tuple)):
            for name in options:
                cname = self._clean_name(name)
                self.options[cname] = self._normalize_option_conf(
                    cname,
                    {"aliases": [
                        f"--{cname.replace('_','-')}"], "action": "store_true"},
                )
        else:
            raise TypeError("options must be dict or list")

        self.flag_to_name = {}
        for cname, conf in self.options.items():
            for flag in conf["aliases"]:
                if not isinstance(flag, str) or not flag.startswith("-"):
                    raise ValueError(
                        f"Invalid alias '{flag}' for option '{cname}'")
                if flag in self.flag_to_name and self.flag_to_name[flag] != cname:
                    raise ValueError(
                        f"Alias '{flag}' is duplicated for different options")
                self.flag_to_name[flag] = cname

        self.positionals = []
        self.positional_index = []
        if not isinstance(arguments, (list, tuple)):
            raise TypeError("arguments must be list/tuple")
        for idx, spec in enumerate(arguments):
            if isinstance(spec, str):
                conf = {"name": self._clean_name(
                    spec), "default": None, "required": True, "multiple": False}
            elif isinstance(spec, tuple) and len(spec) == 2:
                conf = {"name": self._clean_name(
                    spec[0]), "default": spec[1], "required": spec[1] is None, "multiple": False}
            elif isinstance(spec, dict) and "name" in spec:
                conf = {
                    "name": self._clean_name(spec["name"]),
                    "default": spec.get("default", None),
                    "required": bool(spec.get("required", spec.get("default", None) is None and not spec.get("multiple", False))),
                    "multiple": bool(spec.get("multiple", False)),
                    "type": spec.get("type", str),
                    "choices": spec.get("choices"),
                }
            else:
                raise ValueError(
                    f"Invalid positional spec at index {idx}: {spec!r}")
            if conf.get("multiple", False) and idx != len(arguments) - 1:
                raise ValueError(
                    "Only the last positional argument may have multiple=True")
            self.positionals.append(conf)
            self.positional_index.append(conf["name"])

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        if not isinstance(argument_list, (list, tuple)):
            raise TypeError("argument_list must be list/tuple of strings")
        tokens = list(argument_list)
        result = {}

        # Initialize with defaults for options
        for name, conf in self.options.items():
            if conf["action"] == "store_true":
                result[name] = conf.get("default", False)
            elif conf["action"] == "store_false":
                result[name] = conf.get("default", True)
            elif conf["action"] == "count":
                result[name] = conf.get("default", 0) or 0
            elif conf["action"] == "append":
                result[name] = list(conf.get("default", []))
            else:
                result[name] = conf.get("default", None)

        # Initialize positionals with defaults
        for conf in self.positionals:
            if conf.get("multiple", False):
                result[conf["name"]] = list(conf.get("default", []))
            else:
                result[conf["name"]] = conf.get("default", None)

        # Parse options and collect positional tokens
        pos_values = []
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if isinstance(tok, str) and tok.startswith("-") and tok != "-":
                # Long with = : --key=value
                if tok.startswith("--") and "=" in tok:
                    flag, val = tok.split("=", 1)
                    self._apply_option(flag, val, result)
                    i += 1
                    continue

                # Handle --no-<flag> for booleans
                if tok.startswith("--no-"):
                    base = "--" + tok[5:]
                    cname = self.flag_to_name.get(base)
                    if not cname:
                        raise ValueError(f"Unknown option '{tok}'")
                    conf = self.options[cname]
                    if conf["action"] == "store_true":
                        result[cname] = False
                        i += 1
                        continue
                    elif conf["action"] == "store_false":
                        result[cname] = True
                        i += 1
                        continue
                    else:
                        raise ValueError(
                            f"Option '{base}' does not support negation form '{tok}'")

                # Regular flag possibly expecting value
                cname = self.flag_to_name.get(tok)
                if not cname:
                    raise ValueError(f"Unknown option '{tok}'")
                conf = self.options[cname]
                action = conf["action"]

                if action in ("store_true", "store_false"):
                    result[cname] = True if action == "store_true" else False
                    i += 1
                    continue
                if action == "count":
                    result[cname] = (result.get(cname, 0) or 0) + 1
                    i += 1
                    continue

                # Needs a value
                if i + 1 >= len(tokens):
                    raise ValueError(f"Option '{tok}' requires a value")
                value_token = tokens[i + 1]
                self._apply_option(tok, value_token, result)
                i += 2
            else:
                pos_values.append(tok)
                i += 1

        # Assign positional values
        pi = 0
        for conf in self.positionals:
            name = conf["name"]
            multiple = conf.get("multiple", False)
            ptype = conf.get("type", str)
            choices = conf.get("choices")

            if multiple:
                rest = pos_values[pi:]
                converted = [self._convert_value(
                    v, ptype, f"positional '{name}'") for v in rest]
                if choices is not None:
                    for v in converted:
                        if v not in choices:
                            raise ValueError(
                                f"Invalid value for positional '{name}': {v!r}. Allowed: {list(choices)!r}")
                result[name] = converted
                pi = len(pos_values)
            else:
                if pi >= len(pos_values):
                    if conf.get("required", True) and result.get(name) is None:
                        raise ValueError(
                            f"Missing required positional argument '{name}'")
                    # keep default
                else:
                    val = self._convert_value(
                        pos_values[pi], ptype, f"positional '{name}'")
                    if choices is not None and val not in choices:
                        raise ValueError(
                            f"Invalid value for positional '{name}': {val!r}. Allowed: {list(choices)!r}")
                    result[name] = val
                    pi += 1

        if pi < len(pos_values):
            extra = pos_values[pi:]
            raise ValueError(f"Unexpected positional arguments: {extra!r}")

        # Validate required options
        for name, conf in self.options.items():
            if conf.get("required") and (result.get(name) is None or (conf["action"] == "append" and not result.get(name))):
                raise ValueError(
                    f"Missing required option '--{name.replace('_','-')}'")

        return result

    def _clean_name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be string")
        name = name.strip()
        if name.startswith("-"):
            name = name.lstrip("-")
        return name.replace("-", "_")

    def _normalize_option_conf(self, name, conf):
        cname = self._clean_name(name)
        norm = {}
        norm["aliases"] = list(conf.get("aliases") or [
                               f"--{cname.replace('_','-')}"])
        # Ensure canonical long alias exists
        long_alias = f"--{cname.replace('_','-')}"
        if long_alias not in norm["aliases"]:
            norm["aliases"].append(long_alias)

        action = conf.get("action")
        if action not in (None, "store", "store_true", "store_false", "count", "append"):
            raise ValueError(
                f"Unsupported action for option '{cname}': {action}")
        if action is None:
            if conf.get("type", str) is bool or isinstance(conf.get("default", None), bool):
                action = "store_true"
            else:
                action = "store"
        norm["action"] = action
        norm["type"] = conf.get("type", (None if action in (
            "store_true", "store_false", "count") else str))
        norm["default"] = conf.get("default", (False if action == "store_true" else True if action ==
                                   "store_false" else 0 if action == "count" else ([] if action == "append" else None)))
        norm["required"] = bool(conf.get("required", False))
        norm["choices"] = conf.get("choices")
        return norm

    def _convert_value(self, value, typ, ctx):
        if typ is None:
            return value
        try:
            return typ(value)
        except Exception as e:
            raise ValueError(
                f"Invalid value for {ctx}: {value!r} ({e})") from None

    def _apply_option(self, flag, raw_value, result_dict):
        cname = self.flag_to_name.get(flag)
        if not cname:
            raise ValueError(f"Unknown option '{flag}'")
        conf = self.options[cname]
        action = conf["action"]

        if action in ("store_true", "store_false", "count"):
            raise ValueError(f"Option '{flag}' does not take a value")

        if action == "append":
            val = self._convert_value(raw_value, conf.get(
                "type", str), f"option '{flag}'")
            if conf.get("choices") is not None and val not in conf["choices"]:
                raise ValueError(
                    f"Invalid value for option '{flag}': {val!r}. Allowed: {list(conf['choices'])!r}")
            result_dict[cname].append(val)
            return

        # action == "store"
        val = self._convert_value(raw_value, conf.get(
            "type", str), f"option '{flag}'")
        if conf.get("choices") is not None and val not in conf["choices"]:
            raise ValueError(
                f"Invalid value for option '{flag}': {val!r}. Allowed: {list(conf['choices'])!r}")
        result_dict[cname] = val
