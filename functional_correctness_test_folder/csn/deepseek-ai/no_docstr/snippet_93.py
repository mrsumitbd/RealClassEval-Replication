
class PipelineInfo:

    def __init__(self, pipeline_name, loader, parent, is_parent_cascading=True, is_loader_cascading=True):
        self.pipeline_name = pipeline_name
        self.loader = loader
        self.parent = parent
        self.is_parent_cascading = is_parent_cascading
        self.is_loader_cascading = is_loader_cascading

    def __eq__(self, other):
        if not isinstance(other, PipelineInfo):
            return False
        return (
            self.pipeline_name == other.pipeline_name and
            self.loader == other.loader and
            self.parent == other.parent and
            self.is_parent_cascading == other.is_parent_cascading and
            self.is_loader_cascading == other.is_loader_cascading
        )
