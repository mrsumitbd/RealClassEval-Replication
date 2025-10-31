import warnings

class FSM:
    """
    Pass callables for matcher and handler to add_handler to create
    transitions between states. A "matcher" is a predicate, and if a
    transition handles something, it returns the next state.

    If you want something to track global state, put it in your data
    instance passed to process so that transitions and states can
    access it.

    Example:
    idle = State("IDLE")
    stuff = State("STUFF")

    def is_capital(letter):
        return letter in string.uppercase

    def is_small(letter):
        return letter in string.lowercase

    def do_something_with_capitals(letter):
        print("Got capital:", letter)
        return stuff

    idle.add_transition(
        Transition(stuff, is_capital, self.do_something_with_capitals)
    )
    stuff.add_transition(
        Transition(idle, is_lower, None)
    )
    """
    states = []
    state = None

    def __init__(self, states):
        """first state is the initial state"""
        if len(states) > 0:
            self.state = states[0]
        self.states = states

    def process(self, data):
        if self.state is None:
            raise RuntimeError('There is no initial state.')
        next_state = self.state.process(data)
        if next_state:
            self.state = next_state
        else:
            warnings.warn('No next state', RuntimeWarning)

    def add_state(self, state):
        if len(self.states) == 0:
            self.state = state
        self.states.append(state)

    def dotty(self):
        r = 'digraph fsm {\n\n'
        for s in self.states:
            r = r + s.dotty()
        r = r + '\n}\n'
        return r