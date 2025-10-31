class Node:

    def __init__(self, fully_qualified_name, node_type, file_path, line_start, line_end):
        self.fully_qualified_name = fully_qualified_name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.type = node_type
        self.methods_called_by_me = set()

    def added_method_called_by_me(self, node):
        """Add a calling method to this node."""
        if isinstance(node, Node):
            self.methods_called_by_me.add(node.fully_qualified_name)
        else:
            raise ValueError('Expected a Node instance.')

    def __hash__(self):
        return hash(self.fully_qualified_name)

    def __repr__(self):
        return f'Node({self.fully_qualified_name}, {self.file_path}, {self.line_start}-{self.line_end})'