import __main__

class Completer:
    """
    [FUTURE]
    """

    def __init__(self, namespace=None):
        """Create a new completer for the command line.

        Completer([namespace]) -> completer instance.

        Completer instances should be used as the completion mechanism of
        readline via the set_completer() call:

        readline.set_completer(Completer(my_namespace).complete)
        """
        if namespace and (not isinstance(namespace, dict)):
            raise TypeError('namespace must be a dictionary')
        if namespace is None:
            self.use_main_ns = 1
        else:
            self.use_main_ns = 0
            self.namespace = namespace

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.

        """
        if self.use_main_ns:
            self.namespace = __main__.__dict__
        if state == 0:
            self.matches = self.attr_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def attr_matches(self, text):
        """Compute matches when text contains a dot.

        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluable in self.namespace, it will be evaluated and its attributes
        (as revealed by dir()) are used as possible completions.  (For class
        instances, class members are also considered.)

        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.

        """

        def _method_or_attr(thisobject, item):
            if hasattr(getattr(thisobject, item), '__call__'):
                return item + '('
            else:
                return item
        tb_compl_commands = {'.': {}, '[': {}, '.get(': {}, '.set(': {}, '.filter(': {}, '.filter_or_get(': {}, '.get_parameter(': {}, '.remove_parameter(': {}, '.remove_parameters_all(': {}, '.get_value(': {}, '.set_value(': {}, '.set_value_all(': {}, '.get_history(': {'context': 'history'}, '.remove_history(': {'context': 'history'}, '.get_component(': {'context': 'system'}, '.remove_component(': {'context': 'system'}, '.get_mesh(': {'context': 'mesh'}, '.remove_mesh(': {'context': 'mesh'}, '.get_constraint(': {'context': 'constraint'}, '.remove_constraint(': {'context': 'constraint'}, '.flip_constraint(': {'context': 'constraint'}, '.run_constraint(': {'context': 'constraint'}, '.get_compute(': {'context': 'compute'}, '.remove_compute(': {'context': 'compute'}, '.run_compute(': {'context': 'compute'}, '.get_distribution(': {'context': 'distribution'}, '.sample_distribution(': {'context': 'distribution'}, '.remove_distribution(': {'context': 'distribution'}, '.get_solver(': {'context': 'solver'}, '.remove_solver(': {'context': 'solver'}, '.run_solver(': {'context': 'solver'}, '.get_solution(': {'context': 'solution'}, '.remove_solution(': {'context': 'solution'}}
        expr = None
        for cmd, filter_kwargs in tb_compl_commands.items():
            if cmd in text:
                expr, attr = text.rsplit(cmd, 1)
                if attr[0] not in ["'", '"'] and cmd != '.':
                    return []
                else:
                    if cmd == '.':
                        stringchar = ''
                        attr = attr
                    else:
                        stringchar = attr[0]
                        attr = attr[1:]
                    break
        if expr is None:
            return []
        try:
            thisobject = eval(expr, self.namespace)
        except Exception:
            return []
        if cmd == '.':
            words = [_method_or_attr(thisobject, item) for item in dir(thisobject) if item[:len(attr)] == attr]
        else:
            words = thisobject.filter_or_get(attr, autocomplete=True, **filter_kwargs)
        matches = []
        n = len(attr)
        for word in words:
            matches.append('{}{}{}{}'.format(expr, cmd, stringchar, word))
        return matches