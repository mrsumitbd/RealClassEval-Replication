
class ArgFilterBase:

    def maybe_set_arg_name(self, arg_name):
        self.arg_name = arg_name

    def filter_query(self, query, view, arg_value):
        raise NotImplementedError(
            "This method should be overridden by subclasses.")
