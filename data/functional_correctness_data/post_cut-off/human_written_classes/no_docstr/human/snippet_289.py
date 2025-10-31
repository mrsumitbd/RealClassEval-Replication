from typing import Optional, Any, List

class RLPayload:
    payload: Any

    def __init__(self, payload: Any):
        self.payload = payload

    @staticmethod
    def collate_fn(batch: List[tuple[int, 'RLPayload', str]]) -> tuple[List[int], List['RLPayload'], List[str]]:
        return ([item[0] for item in batch], [item[1] for item in batch])