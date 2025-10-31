from pypyr.pipedef import PipelineDefinition, PipelineInfo
from pypyr.cache.cache import Cache
from collections.abc import Mapping
from pypyr.errors import PipelineDefinitionError

class Loader:
    """A single pipeline loader & the cache for all pipelines it has loaded.

    It loads pipelines using the get_pipeline_definition you assign to the
    loader at initialization.

    Attributes:
        name (str): Absolute module name of loader.
    """
    __slots__ = ['name', '_get_pipeline_definition', '_pipeline_cache']

    def __init__(self, name, get_pipeline_definition):
        """Initialize the loader and its pipeline cache.

        The expected function signature is:
        get_pipeline_definition(name: str,
                                parent: any) -> PipelineDefinition | Mapping

        Args:
            name: Absolute name of loader
            get_pipeline_definition: Reference to the function to call when
                loading a pipeline with this Loader.
        """
        self.name = name
        self._get_pipeline_definition = get_pipeline_definition
        self._pipeline_cache = Cache()

    def clear(self):
        """Clear all the pipelines in this Loader's cache."""
        self._pipeline_cache.clear()

    def get_pipeline(self, name, parent):
        """Get cached PipelineDefinition. Adds it to cache if it doesn't exist.

        The cache is local to this Loader instance.

        The combination of parent+name must be unique for this Loader. Parent
        should therefore have a sensible __str__ implementation because it
        forms part of the pipeline's identifying str key in the cache.

        Args:
            name (str): Name of pipeline, sans .yaml at end.
            parent (any): Parent in which to look for pipeline.

        Returns:
            pypyr.pipedef.PipelineDefinition: Yaml payload and loader info
                metadata for the pipeline.
        """
        normalized_name = f'{parent}+{name}' if parent else name
        return self._pipeline_cache.get(normalized_name, lambda: self._load_pipeline(name, parent))

    def _load_pipeline(self, name, parent):
        """Execute get_pipeline_definition(name, parent) for this loader.

        If the loader get_pipeline_definition does not return a
        PipelineDefinition, this method will wrap the payload inside a
        PipelineDefinition for you.

        Args:
            name (str): Name of pipeline, sans .yaml at end.
            parent (any): Parent in which to look for pipeline.

        Returns:
            pypyr.pipedef.PipelineDefinition: Yaml payload and loader info
                metadata for the pipeline.
        """
        logger.debug('starting')
        logger.debug('loading the pipeline definition with %s', self.name)
        pipeline_definition = self._get_pipeline_definition(pipeline_name=name, parent=parent)
        if not isinstance(pipeline_definition, PipelineDefinition):
            pipeline_definition = PipelineDefinition(pipeline=pipeline_definition, info=PipelineInfo(pipeline_name=name, loader=self.name, parent=parent))
        if not isinstance(pipeline_definition.pipeline, Mapping):
            raise PipelineDefinitionError("A pipeline must be a mapping at the top level. Does your top-level yaml have a 'steps:' key? For example:\n\nsteps:\n  - name: pypyr.steps.echo\n    in:\n      echoMe: this is a bare bones pipeline example.\n")
        logger.debug('done')
        return pipeline_definition