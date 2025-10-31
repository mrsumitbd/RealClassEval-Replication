class PipelineDefinition:
    """The pipeline body and its metadata.

    A loader creates the PipelineDefinition and sets the metadata in .info.

    The PipelineDefinition is a globally shared cache of the pipeline body &
    meta-data.

    Attributes:
        pipeline (dict-like): The pipeline yaml body.
        info (PipelineInfo): Meta-data set by the loader for the pipeline.
    """
    __slots__ = ['pipeline', 'info']

    def __init__(self, pipeline, info):
        """Initialize a pipeline definition.

        Args:
            pipeline (dict-like): The pipeline yaml body itself.
            info (PipelineInfo): Meta-data set by the loader for the pipeline.
        """
        self.pipeline = pipeline
        self.info = info

    def __eq__(self, other):
        """Equality comparison checks Pipeline and info objects are equal."""
        type_self = type(self)
        if type_self is type(other):
            all_slots = [p for c in type_self.__mro__ for p in getattr(c, '__slots__', [])]
            return all((getattr(self, s, id(self)) == getattr(other, s, id(other)) for s in all_slots))
        else:
            return False