
class PipelineInfo:
    '''The common attributes that every pipeline loader should set.
    Custom loaders that want to add more properties to a pipeline's meta-data
    should probably derive from this class.
    Attributes:
        pipeline_name (str): Name of pipeline, as set by the loader.
        loader (str): Absolute module name of the pipeline loader.
        parent (any): pipeline_name resolves from parent. The parent can be any
            type - it is up to the loader to interpret the parent property.
        is_loader_cascading (bool): Loader cascades to child pipelines if not
            otherwise set on pype. Default True.
        is_parent_cascading (bool): Parent cascades to child pipelines if not
            otherwise set on pype. Default True.
    '''

    def __init__(self, pipeline_name, loader, parent, is_parent_cascading=True, is_loader_cascading=True):
        self.pipeline_name = pipeline_name
        self.loader = loader
        self.parent = parent
        self.is_parent_cascading = is_parent_cascading
        self.is_loader_cascading = is_loader_cascading

    def __eq__(self, other):
        if not isinstance(other, PipelineInfo):
            return False
        return (self.pipeline_name == other.pipeline_name and
                self.loader == other.loader and
                self.parent == other.parent and
                self.is_parent_cascading == other.is_parent_cascading and
                self.is_loader_cascading == other.is_loader_cascading)
