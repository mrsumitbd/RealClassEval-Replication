from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class AggregateGenerationsLogger:

    def __init__(self, loggers: List[str]):
        self.loggers: List[GenerationLogger] = []
        for logger in loggers:
            if logger in GEN_LOGGERS:
                self.loggers.append(GEN_LOGGERS[logger]())

    def log(self, samples: List[Tuple[str, str, str, float]], step: int) -> None:
        for logger in self.loggers:
            logger.log(samples, step)