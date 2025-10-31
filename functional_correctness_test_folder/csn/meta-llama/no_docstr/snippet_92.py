
class PipelineDefinition:

    def __init__(self, pipeline, info):
        """
        Initialize a PipelineDefinition object.

        Args:
            pipeline (object): The pipeline object.
            info (dict): Additional information about the pipeline.
        """
        self.pipeline = pipeline
        self.info = info

    def __eq__(self, other):
        """
        Check if two PipelineDefinition objects are equal.

        Args:
            other (PipelineDefinition): The other PipelineDefinition object.

        Returns:
            bool: True if the two objects are equal, False otherwise.
        """
        if not isinstance(other, PipelineDefinition):
            return False
        return self.pipeline == other.pipeline and self.info == other.info
