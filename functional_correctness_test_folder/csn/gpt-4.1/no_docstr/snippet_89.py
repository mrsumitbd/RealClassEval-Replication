
class Loader:

    def __init__(self, name, get_pipeline_definition):
        self.name = name
        self.get_pipeline_definition = get_pipeline_definition
        self._cache = {}

    def clear(self):
        self._cache.clear()

    def get_pipeline(self, name, parent):
        key = (name, id(parent))
        if key not in self._cache:
            self._cache[key] = self._load_pipeline(name, parent)
        return self._cache[key]

    def _load_pipeline(self, name, parent):
        definition = self.get_pipeline_definition(name)
        if definition is None:
            raise ValueError(f"Pipeline definition for '{name}' not found.")
        # For demonstration, let's assume the pipeline is just the definition and parent
        return {'name': name, 'definition': definition, 'parent': parent}
