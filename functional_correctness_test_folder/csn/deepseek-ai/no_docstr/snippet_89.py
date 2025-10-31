
class Loader:

    def __init__(self, name, get_pipeline_definition):
        self.name = name
        self.get_pipeline_definition = get_pipeline_definition
        self.pipelines = {}

    def clear(self):
        self.pipelines.clear()

    def get_pipeline(self, name, parent):
        if name not in self.pipelines:
            self._load_pipeline(name, parent)
        return self.pipelines[name]

    def _load_pipeline(self, name, parent):
        pipeline_def = self.get_pipeline_definition(name)
        self.pipelines[name] = pipeline_def(parent)
