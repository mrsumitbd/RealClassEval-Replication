class WorkerMeta:
    keys = ['WORLD_SIZE', 'RANK', 'LOCAL_WORLD_SIZE', 'LOCAL_RANK', 'MASTER_ADDR', 'MASTER_PORT', 'CUDA_VISIBLE_DEVICES']

    def __init__(self, store) -> None:
        self._store = store

    def to_dict(self):
        return {f'_{key.lower()}': self._store.get(f'_{key.lower()}', None) for key in WorkerMeta.keys}