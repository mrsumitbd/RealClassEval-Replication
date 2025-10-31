class PipelineDefinition:
    '''The pipeline body and its metadata.
    A loader creates the PipelineDefinition and sets the metadata in .info.
    The PipelineDefinition is a globally shared cache of the pipeline body &
    meta-data.
    Attributes:
        pipeline (dict-like): The pipeline yaml body.
        info (PipelineInfo): Meta-data set by the loader for the pipeline.
    '''

    def __init__(self, pipeline, info):
        '''Initialize a pipeline definition.
        Args:
            pipeline (dict-like): The pipeline yaml body itself.
            info (PipelineInfo): Meta-data set by the loader for the pipeline.
        '''
        self.pipeline = pipeline
        self.info = info

    def __eq__(self, other):
        '''Equality comparison checks Pipeline and info objects are equal.'''
        if not isinstance(other, PipelineDefinition):
            return NotImplemented
        return self.pipeline == other.pipeline and self.info == other.info
