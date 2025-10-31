from bids.utils import listify, convert_JSON
from bids.modeling import transformations as pbt

class TransformerManager:
    """Handles registration and application of transformations to
    BIDSVariableCollections.

    Parameters
    ----------
    default: object
        A module or other object containing default transformations as
            attributes. Any named transformation not explicitly registered on
            the TransformerManager instance is expected to be found here.
            If None, the PyBIDS transformations module is used.
    keep_history: bool
        Whether to keep snapshots variable after a transformation is applied.
        If True, a list of collections will be stored in the ``history_`` attribute.
    """

    def __init__(self, default=None, keep_history=True):
        self.transformations = {}
        if default in (None, 'pybids-transforms-v1'):
            default = pbt
        self.default = default
        self.keep_history = keep_history

    def _sanitize_name(self, name):
        """ Replace any invalid/reserved transformation names with acceptable
        equivalents.

        Parameters
        ----------
        name: str
            The name of the transformation to sanitize.
        """
        if name in ('And', 'Or'):
            name += '_'
        return name

    def register(self, name, func):
        """Register a new transformation handler.

        Parameters
        ----------
        name : str
            The name of the transformation to handle.
        func : callable
            The callable to invoke when the named transformation is applied.
        """
        name = self._sanitize_name(name)
        self.transformations[name] = func

    def transform(self, collection, transformations):
        """Apply all transformations to the variables in the collection.

        Parameters
        ----------
        collection: BIDSVariableCollection
            The BIDSVariableCollection containing variables to transform.
        transformations : list
            List of transformations to apply.
        """
        if self.keep_history:
            self.history_ = [TransformationOutput(index=0, output=collection.clone(), transformation_name=None, transformation_kwargs=None, input_cols=None, level=None)]
        for ix, t in enumerate(transformations):
            t = convert_JSON(t)
            kwargs = dict(t)
            name = self._sanitize_name(kwargs.pop('name'))
            cols = kwargs.pop('input', None)
            func = self.transformations.get(name, None)
            if func is None:
                if not hasattr(self.default, name):
                    raise ValueError("No transformation '%s' found: either explicitly register a handler, or pass a default module that supports it." % name)
                func = getattr(self.default, name)
                func(collection, cols, **kwargs)
                if self.keep_history:
                    self.history_.append(TransformationOutput(index=ix + 1, output=collection.clone(), transformation_name=name, transformation_kwargs=kwargs, input_cols=cols, level=collection.level))
        return collection