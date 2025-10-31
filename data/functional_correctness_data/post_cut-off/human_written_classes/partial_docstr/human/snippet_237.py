from prime_rl.trainer import envs

class World:
    """This class stores topology information for distributed training and inference settings by parsing environment variables set by torchrun."""

    def __init__(self):
        self.rank = envs.RANK
        self.world_size = envs.WORLD_SIZE
        self.local_rank = envs.LOCAL_RANK
        self.local_world_size = envs.LOCAL_WORLD_SIZE
        self._check_world()
        self.num_nodes = self.world_size // self.local_world_size

    def _check_world(self):
        assert 0 <= self.local_rank < self.local_world_size
        assert 0 <= self.rank < self.world_size
        assert self.local_world_size <= self.world_size
        assert self.world_size % self.local_world_size == 0

    @property
    def is_master(self):
        return self.rank == 0

    def __repr__(self):
        return f'World(world_size={self.world_size}, rank={self.rank}, local_rank={self.local_rank}, local_world_size={self.local_world_size}, num_nodes={self.num_nodes})'