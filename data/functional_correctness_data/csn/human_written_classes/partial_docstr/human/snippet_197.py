import ast

class ModuleDefinition:
    """Handling of a definition."""
    module_definitions = None
    name = None
    node = None
    path = None

    def __init__(self, local_module_definitions, name, parent_module_name, path):
        self.module_definitions = local_module_definitions
        self.parent_module_name = parent_module_name
        self.path = path
        if parent_module_name:
            if isinstance(parent_module_name, ast.alias):
                self.name = parent_module_name.name + '.' + name
            else:
                self.name = parent_module_name + '.' + name
        else:
            self.name = name

    def __str__(self):
        name = 'NoName'
        node = 'NoNode'
        if self.name:
            name = self.name
        if self.node:
            node = str(self.node)
        return 'Path:' + self.path + ' ' + self.__class__.__name__ + ': ' + ';'.join((name, node))