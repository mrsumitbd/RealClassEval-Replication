from typing import Any, Dict, List, Optional, Tuple

class ResourcePool:
    """
    Manages a pool of resources across multiple nodes, tracking process counts and GPU allocations.
    The class provides methods to calculate world size, local world sizes, and local ranks
    across all nodes in the pool.
    """

    def __init__(self, process_on_nodes=None, max_colocate_count: int=10, n_gpus_per_node=8) -> None:
        """Initialize the ResourcePool with node processes and GPU configuration.

        Args:
            process_on_nodes (List[int], optional): List of process counts per node. Defaults to empty list.
            max_colocate_count (int, optional): Maximum number of processes that can be colocated. Defaults to 10.
            n_gpus_per_node (int, optional): Number of GPUs available per node. Defaults to 8.
        """
        if process_on_nodes is None:
            process_on_nodes = []
        self._store = process_on_nodes
        self.max_colocate_count = max_colocate_count
        self.n_gpus_per_node = n_gpus_per_node

    def add_node(self, process_count):
        self._store.append(process_count)

    @property
    def world_size(self):
        """Total number of processes across all nodes in the pool."""
        return sum(self._store)

    def __call__(self) -> Any:
        return self._store

    @property
    def store(self):
        return self._store

    def local_world_size_list(self) -> List[int]:
        """Returns a flat list where each process has its local world size."""
        nested_local_world_size_list = [[local_world_size for _ in range(local_world_size)] for local_world_size in self._store]
        return [item for row in nested_local_world_size_list for item in row]

    def local_rank_list(self) -> List[int]:
        """Returns a flat list of local ranks for all processes across all nodes."""
        nested_local_rank_list = [[i for i in range(local_world_size)] for local_world_size in self._store]
        return [item for row in nested_local_rank_list for item in row]