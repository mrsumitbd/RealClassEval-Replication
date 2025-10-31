
class Loader:

    def __init__(self, name, get_pipeline_definition):
        self.name = name
        self.get_pipeline_definition = get_pipeline_definition
        self.pipeline_cache = {}

    def clear(self):
        self.pipeline_cache.clear()

    def get_pipeline(self, name, parent):
        if name not in self.pipeline_cache:
            self._load_pipeline(name, parent)
        return self.pipeline_cache[name]

    def _load_pipeline(self, name, parent):
        pipeline_definition = self.get_pipeline_definition(name)
        if pipeline_definition is None:
            raise ValueError(f"Pipeline '{name}' not found")
        # Assuming pipeline_definition is a valid pipeline object or can be used to create one
        self.pipeline_cache[name] = pipeline_definition
