from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist

class ProxyModel:
    """
    Wrapper for generating DoesNotExist exceptions without modifying
    the provided model. This is needed by DRF as the views only handle
    the specific exception by the model.
    """

    def __init__(self, model=None):
        self._model = model
        if self._model and (not self._model._meta.abstract):
            self.DoesNotExist = model.DoesNotExist
        else:
            self.DoesNotExist = ObjectDoesNotExist

    def __getattr__(self, name):
        return getattr(self._model, name)