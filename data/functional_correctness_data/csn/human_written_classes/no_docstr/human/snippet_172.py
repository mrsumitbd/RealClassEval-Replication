class CFG:

    def __init__(self, nodes, blackbox_assignments, filename):
        self.nodes = nodes
        self.blackbox_assignments = blackbox_assignments
        self.filename = filename

    def __repr__(self):
        output = ''
        for x, n in enumerate(self.nodes):
            output = ''.join((output, 'Node: ' + str(x) + ' ' + repr(n), '\n\n'))
        return output

    def __str__(self):
        output = ''
        for x, n in enumerate(self.nodes):
            output = ''.join((output, 'Node: ' + str(x) + ' ' + str(n), '\n\n'))
        return output