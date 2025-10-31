class Filter:
    key = None
    display = None
    no_argument = False

    def where_clause(self, table, column, value, param_counter):
        raise NotImplementedError

    def human_clause(self, column, value):
        raise NotImplementedError