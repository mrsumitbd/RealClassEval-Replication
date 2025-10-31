import json

class KernelInfo:
    """Representation of kernel info returned by the notebook's /api/kernel endpoint.

    Attributes
    ----------
    id: str
    name: str
    last_activity: str
    execution_state: str 
    connections: int

    Example
    -------
    ::

        {id: 'f92b7c8b-0858-4d10-903c-b0631540fb36',
        name: 'dev',
        last_activity: '2019-03-14T23:38:08.137987Z',
        execution_state: 'idle',
        connections: 0}
    """

    def __init__(self, *args, id, name, last_activity, execution_state, connections):
        self.model = {'id': id, 'name': name, 'last_activity': last_activity, 'execution_state': execution_state, 'connections': connections}
        self.id = id
        self.name = name
        self.last_activity = last_activity
        self.execution_state = execution_state
        self.connections = connections

    def __repr__(self):
        return json.dumps(self.model, indent=2)

    def __eq__(self, other):
        if isinstance(other, KernelInfo):
            cmp_attrs = [self.id == other.id, self.name == other.name, self.last_activity == other.last_activity, self.execution_state == other.execution_state, self.connections == other.connections]
            return all(cmp_attrs)
        else:
            return False