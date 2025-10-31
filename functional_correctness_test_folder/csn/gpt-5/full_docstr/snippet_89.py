from collections.abc import Mapping


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
        self._get_pipeline_definition = get_pipeline_definition
        self._cache = {}

    def clear(self):
        '''Clear all the pipelines in this Loader's cache.'''
        self._cache.clear()

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
        key = f'{str(parent)}:{name}'
        if key not in self._cache:
            self._cache[key] = self._load_pipeline(name, parent)
        return self._cache[key]

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
        result = self._get_pipeline_definition(name, parent)

        # If already a PipelineDefinition, return as is.
        try:
            from pypyr.pipedef import PipelineDefinition
        except Exception:  # pragma: no cover - only if dependency is missing
            PipelineDefinition = None

        if PipelineDefinition and isinstance(result, PipelineDefinition):
            return result

        # If result is not a Mapping, just return it as-is for compatibility.
        if not isinstance(result, Mapping):
            return result

        # Wrap Mapping in PipelineDefinition with best-effort constructor calls.
        if PipelineDefinition is None:
            # Fall back to returning the mapping if the class isn't available.
            return result

        # Try a series of likely constructor signatures for robustness.
        last_err = None
        try:
            return PipelineDefinition(pipeline=result, name=name, parent=parent, loader=self)
        except Exception as e:
            last_err = e

        try:
            return PipelineDefinition(result, name=name, parent=parent, loader=self)
        except Exception as e:
            last_err = e

        try:
            return PipelineDefinition(result, name, parent, self)
        except Exception as e:
            last_err = e

        try:
            return PipelineDefinition(result)
        except Exception as e:
            last_err = e

        raise TypeError(
            f'Could not construct PipelineDefinition from mapping: {last_err}')
