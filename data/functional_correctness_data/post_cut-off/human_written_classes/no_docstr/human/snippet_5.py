import numpy as np
from typing import Any, Dict, List, Optional, Union

class Memory:

    def __init__(self, memoryId: int, embedding: List[float]=None):
        self.memory_id = memoryId
        if embedding is not None:
            self.embedding = np.array(embedding).squeeze()
        else:
            self.embedding = None

    def to_json(self):
        return {'memoryId': self.memory_id}