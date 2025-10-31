class SpeculatorTPInit:

    def __init__(self):
        self.init_tensor_parallelism()

    def init_tensor_parallelism(self):
        from vllm.distributed.parallel_state import _TP, _SP
        tp_world_size = _TP.world_size
        sp_world_size = _SP.world_size
        self.tp_size = max(tp_world_size, sp_world_size)
        self.tp_rank = _TP.rank % self.tp_size
        self.TP_GROUP = _SP if sp_world_size > tp_world_size else _TP