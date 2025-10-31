class Node:
    """
    # this is a Node of the graph for the shortest path
    """

    def __init__(self, temperatures, timestep):
        self.temperatures = temperatures
        self.timestep = timestep

    def __hash__(self):
        return hash((' '.join((str(e) for e in self.temperatures)), self.timestep))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.temperatures == other.temperatures and (self.timestep == other.timestep)

    def __repr__(self):
        return '{0}-{1}'.format(self.timestep, self.temperatures)