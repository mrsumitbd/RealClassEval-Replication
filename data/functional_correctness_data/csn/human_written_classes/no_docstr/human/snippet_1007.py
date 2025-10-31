class SequenceChoicesEnumMixin:

    def __init__(self, items, initial_states=None):
        assert len(items) > 0
        self.initial_states = initial_states
        super().__init__(*(item[:-1] for item in items if item[0] is not None))
        self.first_choices = self._get_first_choices(items)
        self.sequence_graph = {getattr(self, item[0]): item[-1] for item in items}

    def _get_first_choices(self, items):
        return tuple((getattr(self, key) for key in self.initial_states)) if self.initial_states else self

    def get_allowed_next_states(self, state, instance):
        if not state:
            return self.first_choices
        else:
            states_or_callable = self.sequence_graph.get(state)
            states = states_or_callable(instance) if hasattr(states_or_callable, '__call__') else list(states_or_callable)
            return tuple((getattr(self, next_choice) for next_choice in states))