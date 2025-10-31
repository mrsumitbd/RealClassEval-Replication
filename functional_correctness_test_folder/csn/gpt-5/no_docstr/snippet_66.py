class ArgumentProcessor:

    def __init__(self, options, arguments):
        self.options_raw = options or []
        self.arguments_raw = arguments or []
        self.opt_by_flag = {}
        self.opt_specs = []
        self.positional_specs = []
        self._normalize()

    def _normalize(self):
        def as_list(x):
            if x is None:
                return []
            if isinstance(x, (list, tuple)):
                return list(x)
            return [x]

        # Normalize options
        opts = self.options_raw
        if isinstance(opts, dict):
            # Support dict forms: key->spec or flag->spec
            normalized = []
            for k, v in opts.items():
                spec = dict(v) if isinstance(v, dict) else {}
                # If key looks like a flag, merge into flags
                if isinstance(k, str) and k.startswith("-"):
                    flags = as_list(spec.get("flags")) or []
                    if k not in flags:
                        flags.insert(0, k)
                    spec["flags"] = flags
                else:
                    # Treat as dest name
                    spec["dest"] = spec.get("dest", k)
                normalized.append(spec)
            opts = normalized
        elif not isinstance(opts, list):
            opts = as_list(opts)

        for raw in opts:
            spec = dict(raw) if isinstance(
                raw, dict) else {"flags": as_list(raw)}
            flags = as_list(spec.get("flags")) or as_list(spec.get("flag")) or as_list(
                spec.get("name")) or as_list(spec.get("names"))
            flags = [f for f in flags if isinstance(f, str)]
            if not flags and "dest" not in spec:
                continue
            # Derive dest
            dest = spec.get("dest")
            if not dest:
                # choose longest flag (likely the --long) to derive dest
                longest = max(flags, key=len)
                dest = longest.lstrip("-").replace("-", "_")
            action = spec.get("action")
            if not action:
                # infer action
                if spec.get("has_value") is True or ("type" in spec) or ("choices" in spec) or spec.get("action") == "store":
                    action = "store"
                elif spec.get("action") in ("store_true", "store_false", "append", "count"):
                    action = spec.get("action")
                else:
                    # by default booleans if no type specified
                    action = "store_true"
            has_value = spec.get("has_value")
            if has_value is None:
                has_value = action in ("store", "append")
            typ = spec.get("type")
            if typ is None:
                if action in ("store", "append"):
                    typ = str
                elif action == "count":
                    typ = int
                elif action in ("store_true", "store_false"):
                    typ = bool
            choices = spec.get("choices")
            # Default
            if "default" in spec:
                default = spec["default"]
            else:
                if action == "append":
                    default = []
                elif action == "count":
                    default = 0
                elif action == "store_true":
                    default = False
                elif action == "store_false":
                    default = True
                else:
                    default = None
            ospec = {
                "flags": flags,
                "dest": dest,
                "action": action,
                "has_value": bool(has_value),
                "type": typ,
                "choices": choices,
                "required": bool(spec.get("required", False)),
                "metavar": spec.get("metavar"),
                "help": spec.get("help"),
                "default": default,
            }
            self.opt_specs.append(ospec)
            for fl in flags:
                self.opt_by_flag[fl] = ospec

        # Normalize positionals
        args = self.arguments_raw
        if isinstance(args, dict):
            # map of name->spec
            normalized = []
            for name, spec in args.items():
                s = dict(spec) if isinstance(spec, dict) else {}
                s["name"] = name
                normalized.append(s)
            args = normalized
        elif not isinstance(args, list):
            args = as_list(args)
        for raw in args:
            if isinstance(raw, str):
                spec = {"name": raw}
            else:
                spec = dict(raw) if isinstance(raw, dict) else {}
            name = spec.get("name")
            if not name:
                continue
            multiple = bool(spec.get("multiple", spec.get(
                "nargs") in ("*", "+", None) and False))
            # Support nargs semantics
            nargs = spec.get("nargs")
            if nargs in ("*", "+"):
                multiple = True
            required = bool(spec.get("required", False))
            if nargs == "+":
                required = True
            ptype = spec.get("type", str)
            default = spec.get("default")
            self.positional_specs.append({
                "name": name,
                "multiple": multiple,
                "required": required,
                "type": ptype,
                "choices": spec.get("choices"),
                "default": default,
            })

    def _convert(self, value, typ, flag_for_error=None):
        if typ is None:
            return value
        if typ is bool:
            v = str(value).strip().lower()
            if v in ("1", "true", "t", "yes", "y", "on"):
                return True
            if v in ("0", "false", "f", "no", "n", "off"):
                return False
            raise ValueError(
                f"Invalid boolean value for {flag_for_error or ''}: {value}")
        try:
            return typ(value)
        except Exception as e:
            raise ValueError(
                f"Invalid value {value!r} for {flag_for_error or 'argument'}: {e}") from None

    def _apply_option(self, result, spec, value, flag_for_error=None):
        action = spec["action"]
        dest = spec["dest"]
        if action == "store_true":
            result[dest] = True
            return
        if action == "store_false":
            result[dest] = False
            return
        if action == "count":
            result[dest] = int(result.get(dest, 0)) + 1
            return
        if action == "append":
            if value is None:
                raise ValueError(
                    f"Option {flag_for_error or dest} requires a value")
            v = self._convert(value, spec["type"], flag_for_error)
            if spec.get("choices") and v not in spec["choices"]:
                raise ValueError(
                    f"Option {flag_for_error or dest} must be one of {spec['choices']}")
            lst = result.get(dest)
            if lst is None:
                lst = []
            result.setdefault(dest, lst).append(v)
            return
        # store
        if value is None:
            raise ValueError(
                f"Option {flag_for_error or dest} requires a value")
        v = self._convert(value, spec["type"], flag_for_error)
        if spec.get("choices") and v not in spec["choices"]:
            raise ValueError(
                f"Option {flag_for_error or dest} must be one of {spec['choices']}")
        result[dest] = v

    def process(self, argument_list):
        argv = list(argument_list or [])
        # Initialize result with defaults
        result = {}
        for spec in self.opt_specs:
            d = spec["default"]
            # copy lists to avoid mutation bleed
            if isinstance(d, list):
                result[spec["dest"]] = list(d)
            else:
                result[spec["dest"]] = d
        for ps in self.positional_specs:
            if ps["multiple"]:
                result[ps["name"]] = list(ps["default"] or [])
            elif "default" in ps and ps["default"] is not None:
                result[ps["name"]] = ps["default"]

        i = 0
        positional_tokens = []
        end_of_opts = False
        while i < len(argv):
            tok = argv[i]
            if end_of_opts:
                positional_tokens.append(tok)
                i += 1
                continue
            if tok == "--":
                end_of_opts = True
                i += 1
                continue
            if tok.startswith("--"):
                if tok == "--":
                    i += 1
                    end_of_opts = True
                    continue
                if "=" in tok:
                    flag, val = tok.split("=", 1)
                else:
                    flag, val = tok, None
                spec = self.opt_by_flag.get(flag)
                if not spec:
                    raise ValueError(f"Unknown option: {flag}")
                if spec["has_value"]:
                    if val is None:
                        i += 1
                        if i >= len(argv):
                            raise ValueError(f"Option {flag} requires a value")
                        val = argv[i]
                    self._apply_option(result, spec, val, flag)
                else:
                    self._apply_option(result, spec, None, flag)
                i += 1
                continue
            if tok.startswith("-") and tok != "-":
                # short flags, may be cluster
                if len(tok) > 2 and not tok.startswith("--"):
                    # cluster or attached value
                    j = 1
                    consumed = False
                    while j < len(tok):
                        short_flag = "-" + tok[j]
                        spec = self.opt_by_flag.get(short_flag)
                        if not spec:
                            raise ValueError(f"Unknown option: {short_flag}")
                        if spec["has_value"]:
                            # attached value remainder
                            remainder = tok[j + 1:]
                            if remainder:
                                val = remainder
                                self._apply_option(
                                    result, spec, val, short_flag)
                                consumed = True
                                break
                            else:
                                # take next argv
                                i += 1
                                if i >= len(argv):
                                    raise ValueError(
                                        f"Option {short_flag} requires a value")
                                val = argv[i]
                                self._apply_option(
                                    result, spec, val, short_flag)
                                consumed = True
                                break
                        else:
                            self._apply_option(result, spec, None, short_flag)
                            j += 1
                    i += 1
                    if consumed:
                        # already consumed current or next as value
                        continue
                    else:
                        continue
                else:
                    # single short, may be -oVALUE or -o=VALUE
                    flag = tok[:2]
                    spec = self.opt_by_flag.get(flag)
                    if not spec:
                        raise ValueError(f"Unknown option: {flag}")
                    val = None
                    attached = tok[2:]
                    if spec["has_value"]:
                        if attached.startswith("="):
                            val = attached[1:]
                        elif attached:
                            val = attached
                        else:
                            i += 1
                            if i >= len(argv):
                                raise ValueError(
                                    f"Option {flag} requires a value")
                            val = argv[i]
                        self._apply_option(result, spec, val, flag)
                    else:
                        self._apply_option(result, spec, None, flag)
                    i += 1
                    continue
            # positional
            positional_tokens.append(tok)
            i += 1

        # Assign positionals
        idx = 0
        for ps in self.positional_specs:
            name = ps["name"]
            if ps["multiple"]:
                remaining = positional_tokens[idx:]
                values = []
                for v in remaining:
                    cv = self._convert(v, ps["type"], name)
                    if ps.get("choices") and cv not in ps["choices"]:
                        raise ValueError(
                            f"Argument {name} must be one of {ps['choices']}")
                    values.append(cv)
                result[name] = values
                idx = len(positional_tokens)
                break
            else:
                if idx >= len(positional_tokens):
                    if ps["required"] and ps.get("default") is None:
                        raise ValueError(f"Missing required argument: {name}")
                    # else keep default if any
                    continue
                v = positional_tokens[idx]
                cv = self._convert(v, ps["type"], name)
                if ps.get("choices") and cv not in ps["choices"]:
                    raise ValueError(
                        f"Argument {name} must be one of {ps['choices']}")
                result[name] = cv
                idx += 1
        if idx < len(positional_tokens):
            extras = positional_tokens[idx:]
            raise ValueError(f"Unexpected extra arguments: {extras}")

        # Check required options
        for spec in self.opt_specs:
            if spec["required"] and result.get(spec["dest"]) in (None, [], False, 0):
                # consider falsy but explicit True for store_true is valid
                if spec["action"] == "store_true":
                    if result.get(spec["dest"]) is True:
                        continue
                raise ValueError(
                    f"Missing required option: {'/'.join(spec['flags']) or spec['dest']}")

        return result
