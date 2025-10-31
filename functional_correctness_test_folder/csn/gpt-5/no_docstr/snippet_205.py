class ArgFilterBase:
    def maybe_set_arg_name(self, arg_name):
        current = getattr(self, "arg_name", None)
        if current is None:
            if arg_name is None:
                raise ValueError(
                    "arg_name must be provided or previously set.")
            self.arg_name = arg_name
            return self.arg_name

        if arg_name is not None and arg_name != current:
            raise ValueError(
                f"Conflicting arg_name: existing='{current}', provided='{arg_name}'")
        return current

    def filter_query(self, query, view, arg_value):
        raise NotImplementedError(
            "Subclasses must implement filter_query(query, view, arg_value).")
