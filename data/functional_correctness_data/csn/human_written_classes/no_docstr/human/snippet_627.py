import itertools
from operator import itemgetter

class SecondaryAutomaton:

    def __init__(self, k):
        self.k = k
        self.states = self._build(k)

    def match(self, edges):
        raise NotImplementedError

    @staticmethod
    def _build(k):
        states = dict()
        queue = [frozenset([0])]
        while queue:
            state_id = queue.pop(0)
            state = states[state_id] = dict()
            for i in range(1, 2 ** k):
                new_state = set()
                for t in [2 ** j for j in range(k) if i & 2 ** j]:
                    for v in state_id:
                        new_state.add(t | v)
                new_state = frozenset(new_state - state_id)
                if new_state:
                    if new_state != state_id:
                        state[i] = new_state
                    if new_state not in states and new_state not in queue:
                        queue.append(new_state)
        keys = sorted(states.keys())
        new_states = []
        for state in keys:
            new_states.append(states[state])
        for i, state in enumerate(new_states):
            new_state = dict()
            for key, value in state.items():
                new_state[key] = keys.index(value)
            new_states[i] = new_state
        return new_states

    def as_graph(self):
        if Digraph is None:
            raise ImportError('The graphviz package is required to draw the graph.')
        graph = Digraph()
        for i in range(len(self.states)):
            graph.node(str(i), str(i))
        for state, edges in enumerate(self.states):
            for target, labels in itertools.groupby(sorted(edges.items()), key=itemgetter(1)):
                label = '\n'.join((bin(l)[2:].zfill(self.k) for l, _ in labels))
                graph.edge(str(state), str(target), label)
        return graph