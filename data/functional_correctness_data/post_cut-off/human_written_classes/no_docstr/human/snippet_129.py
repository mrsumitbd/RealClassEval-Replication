from loguru import logger
import pprint
from typing import Any, Dict, List, Union

class ConsoleLogger:

    def __init__(self):
        pass

    def log(self, data: Dict[str, Any], step: int):
        data_as_str = pprint.pformat(ConsoleLogger.stringify_floats(data))
        logger.info(f'Step {step}: \n{data_as_str}')

    def finish(self):
        pass

    @staticmethod
    def stringify_floats(obj: Any) -> Any:
        if isinstance(obj, float):
            return f'{obj:.4f}'
        elif isinstance(obj, dict):
            return {k: ConsoleLogger.stringify_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ConsoleLogger.stringify_floats(v) for v in obj]
        elif isinstance(obj, tuple):
            return tuple((ConsoleLogger.stringify_floats(v) for v in obj))
        return obj