from typing import Any, Callable, Optional

class ResourcePool:
    """The resource pool with meta info such as world size."""

    def __init__(self, process_on_nodes: Optional[Any]=None, max_colocate_count: int=10, n_gpus_per_node: int=8) -> None:
        if process_on_nodes is None:
            process_on_nodes = []
        self._store = process_on_nodes
        self.max_colocate_count = max_colocate_count
        self.n_gpus_per_node = n_gpus_per_node

    def add_node(self, process_count):
        self._store.append(process_count)

    @property
    def world_size(self):
        return sum(self._store)

    def __call__(self) -> Any:
        return self._store

    @property
    def store(self):
        return self._store

    def local_world_size_list(self) -> list[int]:
        nested_local_world_size_list = [[local_world_size for _ in range(local_world_size)] for local_world_size in self._store]
        return [item for row in nested_local_world_size_list for item in row]

    def local_rank_list(self) -> list[int]:
        nested_local_rank_list = [[i for i in range(local_world_size)] for local_world_size in self._store]
        return [item for row in nested_local_rank_list for item in row]