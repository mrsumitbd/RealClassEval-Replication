
class ArgFilterBase:

    def maybe_set_arg_name(self, arg_name):
        self.arg_name = arg_name

    def filter_query(self, query, view, arg_value):
        if hasattr(view, 'filter_query'):
            return view.filter_query(query, arg_value)
        return query
