class ForLoopSimulator:
    """
    Simulates a forloop tag, precisely::

        {% for form in formset.forms %}

    If `{% crispy %}` is rendering a formset with a helper, We inject a `ForLoopSimulator` object
    in the context as `forloop` so that formset forms can do things like::

        Fieldset("Item {{ forloop.counter }}", [...])
        HTML("{% if forloop.first %}First form text{% endif %}"
    """

    def __init__(self, formset):
        self.len_values = len(formset.forms)
        self.counter = 1
        self.counter0 = 0
        self.revcounter = self.len_values
        self.revcounter0 = self.len_values - 1
        self.first = True
        self.last = 0 == self.len_values - 1

    def iterate(self):
        """
        Updates values as if we had iterated over the for
        """
        self.counter += 1
        self.counter0 += 1
        self.revcounter -= 1
        self.revcounter0 -= 1
        self.first = False
        self.last = self.revcounter0 == self.len_values - 1