class ChildScopeBuilder:

    def __init__(self, injector, parent, name):
        self.injector = injector
        self.name = name
        self.parent = parent

    def __enter__(self):
        self.scope = Scope(self.name, self.parent)
        self.injector.add_scope(self.scope)
        return self.scope

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scope.clear()
        self.injector.remove_scope(self.scope)