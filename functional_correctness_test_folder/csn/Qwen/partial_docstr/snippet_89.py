
class Loader:
    '''A single pipeline loader & the cache for all pipelines it has loaded.
    It loads pipelines using the get_pipeline_definition you assign to the
    loader at initialization.
    Attributes:
        name (str): Absolute module name of loader.
    '''

    def __init__(self, name, get_pipeline_definition):
        '''Initialize the loader and its pipeline cache.
        The expected function signature is:
        get_pipeline_definition(name: str,
                                parent: any) -> PipelineDefinition | Mapping
        Args:
            name: Absolute name of loader
            get_pipeline_definition: Reference to the function to call when
                loading a pipeline with this Loader.
        '''
        self.name = name
        self.get_pipeline_definition = get_pipeline_definition
        self._pipeline_cache = {}

    def clear(self):
        '''Clear all the pipelines in this Loader's cache.'''
        self._pipeline_cache.clear()

    def get_pipeline(self, name, parent):
        '''Get cached PipelineDefinition. Adds it to cache if it doesn't exist.
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
        '''
        key = f"{str(parent)}:{name}"
        if key not in self._pipeline_cache:
            self._pipeline_cache[key] = self._load_pipeline(name, parent)
        return self._pipeline_cache[key]

    def _load_pipeline(self, name, parent):
        '''Execute get_pipeline_definition(name, parent) for this loader.
        If the loader get_pipeline_definition does not return a
        PipelineDefinition, this method will wrap the payload inside a
        PipelineDefinition for you.
        Args:
            name (str): Name of pipeline, sans .yaml at end.
            parent (any): Parent in which to look for pipeline.
        Returns:
            pypyr.pipedef.PipelineDefinition: Yaml payload and loader info
                metadata for the pipeline.
        '''
        from pypyr.pipedef import PipelineDefinition

        payload = self.get_pipeline_definition(name, parent)
        if not isinstance(payload, PipelineDefinition):
            payload = PipelineDefinition(payload, self.name)
        return payload
