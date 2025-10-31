class ArgumentProcessor:
    '''
    responsible for parsing given list of arguments
    '''

    def __init__(self, options, arguments):
        '''
        :param options: list of options
        :param arguments: list of arguments
        '''
        def _norm(name: str) -> str:
            name = name.lstrip('-').strip()
            return name.replace('-', '_')

        self.options = set(_norm(o) for o in (options or []))
        self.arguments = [_norm(a) for a in (arguments or [])]

    def _norm(self, name: str) -> str:
        return name.lstrip('-').replace('-', '_')

    def _coerce(self, value):
        if isinstance(value, bool):
            return value
        if not isinstance(value, str):
            return value
        s = value.strip()
        low = s.lower()
        if low in ('true', 'yes', 'y', 'on'):
            return True
        if low in ('false', 'no', 'n', 'off'):
            return False
        # int
        try:
            if s.startswith(('0x', '0X')):
                return int(s, 16)
            if s.startswith(('0o', '0O')):
                return int(s, 8)
            if s.startswith(('0b', '0B')):
                return int(s, 2)
            return int(s)
        except ValueError:
            pass
        # float
        try:
            return float(s)
        except ValueError:
            pass
        return s

    def _is_opt_allowed(self, name: str) -> bool:
        # If no options were declared, accept any option.
        return (not self.options) or (name in self.options)

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        res = {}
        extra_positionals = []
        i = 0
        pos_idx = 0
        n = len(argument_list)
        end_of_opts = False

        def set_value(key, value):
            k = self._norm(key)
            if not self._is_opt_allowed(k):
                return
            res[k] = self._coerce(value)

        while i < n:
            tok = argument_list[i]

            if end_of_opts:
                # treat as positional
                if pos_idx < len(self.arguments):
                    res[self.arguments[pos_idx]] = self._coerce(tok)
                    pos_idx += 1
                else:
                    extra_positionals.append(self._coerce(tok))
                i += 1
                continue

            if tok == '--':
                end_of_opts = True
                i += 1
                continue

            if tok.startswith('--'):
                # long option
                body = tok[2:]
                if body.startswith('no-') and '=' not in body:
                    name = self._norm(body[3:])
                    set_value(name, False)
                    i += 1
                    continue

                if '=' in body:
                    name, val = body.split('=', 1)
                    set_value(name, val)
                    i += 1
                    continue

                name = body
                # lookahead for value
                if i + 1 < n and not argument_list[i + 1].startswith('-'):
                    set_value(name, argument_list[i + 1])
                    i += 2
                else:
                    set_value(name, True)
                    i += 1
                continue

            if tok.startswith('-') and tok != '-':
                body = tok[1:]

                # handle -o=value
                if '=' in body:
                    head, val = body.split('=', 1)
                    # if bundled before '=', set them true, last gets val
                    if len(head) > 1:
                        for ch in head[:-1]:
                            set_value(ch, True)
                        set_value(head[-1], val)
                    else:
                        set_value(head, val)
                    i += 1
                    continue

                # short flags, possibly bundled
                if len(body) == 1:
                    name = body
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        set_value(name, argument_list[i + 1])
                        i += 2
                    else:
                        set_value(name, True)
                        i += 1
                else:
                    # bundled like -abc; last may take next as value
                    for ch in body[:-1]:
                        set_value(ch, True)
                    last = body[-1]
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        set_value(last, argument_list[i + 1])
                        i += 2
                    else:
                        set_value(last, True)
                        i += 1
                continue

            # positional
            if pos_idx < len(self.arguments):
                res[self.arguments[pos_idx]] = self._coerce(tok)
                pos_idx += 1
            else:
                extra_positionals.append(self._coerce(tok))
            i += 1

        # fill any missing positionals with None (optional)
        # Do not overwrite if already set via options
        while pos_idx < len(self.arguments):
            name = self.arguments[pos_idx]
            if name not in res:
                res[name] = None
            pos_idx += 1

        if extra_positionals:
            res['_extra'] = extra_positionals

        return res
