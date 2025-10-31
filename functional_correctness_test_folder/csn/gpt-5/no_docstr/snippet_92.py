class PipelineDefinition:

    def __init__(self, pipeline, info):
        self.pipeline = pipeline
        self.info = info

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, PipelineDefinition):
            return NotImplemented
        return self.pipeline == other.pipeline and self.info == other.info
