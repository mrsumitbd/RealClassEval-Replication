class PipelineDefinition:

    def __init__(self, pipeline, info):
        self.pipeline = pipeline
        self.info = info

    def __eq__(self, other):
        if not isinstance(other, PipelineDefinition):
            return False
        return self.pipeline == other.pipeline and self.info == other.info
