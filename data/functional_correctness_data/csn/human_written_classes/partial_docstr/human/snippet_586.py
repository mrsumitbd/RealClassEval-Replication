import numpy as np
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

class _NumPyBackendContext:
    """This class is internally used in NumPyBackend"""

    def __init__(self, n_qubits: int, cache: Optional[np.ndarray]=None, cache_idx: int=-1) -> None:
        self.n_qubits = n_qubits
        self.qubits = np.zeros(2 ** n_qubits, dtype=DEFAULT_DTYPE)
        self.qubits_buf = np.zeros(2 ** n_qubits, dtype=DEFAULT_DTYPE)
        self.indices = np.arange(2 ** n_qubits, dtype=np.uint32)
        self.save_ctx_cache = True
        self.cache = cache
        self.cache_idx = cache_idx
        self.shots_result = Counter()
        self.cregs = [0] * self.n_qubits

    def prepare(self, initial: Optional[np.ndarray]) -> None:
        """Prepare to run next shot."""
        if self.cache is not None:
            np.copyto(self.qubits, self.cache)
        elif initial is not None:
            np.copyto(self.qubits, initial)
        else:
            self.qubits.fill(0.0)
            self.qubits[0] = 1.0
        self.cregs = [0] * self.n_qubits
        self.sample = {}

    def store_shot(self) -> None:
        """Store current cregs to shots_result"""

        def to_str(cregs: List[int]) -> str:
            return ''.join((str(b) for b in cregs))
        key = to_str(self.cregs)
        self.shots_result[key] = self.shots_result.get(key, 0) + 1