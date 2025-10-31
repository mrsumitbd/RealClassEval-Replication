
class ArgFilterBase:

    def __init__(self):
        self.arg_name = None

    def maybe_set_arg_name(self, arg_name):
        if self.arg_name is None:
            self.arg_name = arg_name

    def filter_query(self, query, view, arg_value):
        raise NotImplementedError("Subclasses must implement filter_query")
