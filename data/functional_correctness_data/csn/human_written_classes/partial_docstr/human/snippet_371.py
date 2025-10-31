from typing import Callable, Tuple
from precise.params import inject_params, pr

class CachedDataLoader:
    """
    Class for reloading train data every time the params change

    Args:
        loader: Function that loads the train data (something that calls TrainData.load)
    """

    def __init__(self, loader: Callable):
        self.prev_cache = None
        self.data = None
        self.loader = loader

    def load_for(self, model: str) -> Tuple[list, list]:
        """Injects the model parameters, reloading if they changed, and returning the data"""
        inject_params(model)
        if self.prev_cache != pr.vectorization_md5_hash():
            self.prev_cache = pr.vectorization_md5_hash()
            self.data = self.loader()
        return self.data