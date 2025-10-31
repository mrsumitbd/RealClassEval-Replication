from typing import Callable, Optional
from loguru import logger
from siirl.utils.params import ProfilerArguments
from siirl.utils.extras.import_utils import is_nvtx_available

class DistProfiler:

    def __init__(self, rank: int, config: ProfilerArguments, **kwargs):
        self.config = config
        if self.config.enable and is_nvtx_available():
            self.config.enable = False
            logger.error('!!!!!!!!!!!!!!!Currently only support NPU profiling.!!!!!!!!!!!!!!!')

    def start(self, **kwargs):
        pass

    def stop(self):
        pass

    @staticmethod
    def annotate(message: Optional[str]=None, color: Optional[str]=None, domain: Optional[str]=None, category: Optional[str]=None, **kwargs) -> Callable:

        def decorator(func):
            return func
        return decorator