
class Loader:
    """
    A simple loader that retrieves pipeline definitions via a user-provided
    callback and builds a lightweight pipeline representation.  The loader
    caches pipelines to avoid repeated lookups and supports a parent-child
    relationship between pipelines.
    """

    def __init__(self, name, get_pipeline_definition):
        """
        Parameters
        ----------
        name : str
            The name of the loader instance (used for identification only).
        get_pipeline_definition : Callable[[str], Any]
            A callable that accepts a pipeline name and returns its
            definition (e.g., a dict or any serializable object).  It must
            raise an exception if the pipeline cannot be found.
        """
        self.name = name
        self._get_pipeline_definition = get_pipeline_definition
        self._cache = {}

    def clear(self):
        """
        Clears the internal cache of loaded pipelines.
        """
        self._cache.clear()

    def get_pipeline(self, name, parent=None):
        """
        Retrieve a pipeline by name, loading it if necessary.

        Parameters
        ----------
        name : str
            The name of the pipeline to retrieve.
        parent : dict, optional
            A parent pipeline dict to which this pipeline will be attached
            as a child.  If omitted, the pipeline is considered a root.

        Returns
        -------
        dict
            A dictionary representing the pipeline, containing at least the
            keys 'name', 'definition', 'parent', and 'children'.
        """
        if name in self._cache:
            pipeline = self._cache[name]
            # If a parent is supplied and differs, update the relationship.
            if parent is not None and pipeline.get('parent') is not parent:
                # Remove from old parent if present
                old_parent = pipeline.get('parent')
                if old_parent and pipeline in old_parent.get('children', []):
                    old_parent['children'].remove(pipeline)
                # Attach to new parent
                pipeline['parent'] = parent
                parent.setdefault('children', []).append(pipeline)
            return pipeline

        return self._load_pipeline(name, parent)

    def _load_pipeline(self, name, parent=None):
        """
        Internal helper to load a pipeline definition and construct its
        representation.

        Parameters
        ----------
        name : str
            The name of the pipeline to load.
        parent : dict, optional
            The parent pipeline dict, if any.

        Returns
        -------
        dict
            The constructed pipeline representation.
        """
        definition = self._get_pipeline_definition(name)
        if definition is None:
            raise ValueError(f"Pipeline definition for '{name}' not found.")

        pipeline = {
            'name': name,
            'definition': definition,
            'parent': parent,
            'children': []
        }

        if parent is not None:
            parent.setdefault('children', []).append(pipeline)

        self._cache[name] = pipeline
        return pipeline
