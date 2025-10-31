import ray
import time
from loguru import logger
from dataclasses import dataclass, field
from siirl.workers.base_worker import RayResourcePool

@dataclass
class ResourcePoolManager:
    """
    Define a resource pool specification. Resource pool will be initialized first.
    """
    resource_pool_spec: dict[str, list[int]]
    resource_pool_dict: dict[str, RayResourcePool] = field(default_factory=dict)

    def create_resource_pool(self):
        for resource_pool_name, process_on_nodes in self.resource_pool_spec.items():
            resource_pool = RayResourcePool(process_on_nodes=process_on_nodes, use_gpu=True, max_colocate_count=1, name_prefix=resource_pool_name)
            self.resource_pool_dict[resource_pool_name] = resource_pool
        self._check_resource_available()

    def get_resource_pool(self, resource_pool_name: str) -> RayResourcePool:
        return self.resource_pool_dict.get(resource_pool_name, None)

    def get_n_gpus(self) -> int:
        """Get the number of gpus in this cluster."""
        return sum([n_gpus for process_on_nodes in self.resource_pool_spec.values() for n_gpus in process_on_nodes])

    def _check_resource_available(self, timeout=60, interval=1):
        """
        Checks if the required resources are available in the Ray cluster,
        waiting up to a specified timeout for nodes to become ready.

        Args:
            timeout (int): Maximum time to wait in seconds.
            interval (int): Time to sleep between checks in seconds.
        """
        logger.info(f'Checking for available resources. Will wait for up to {timeout} seconds.')
        start_time = time.time()
        total_required_gpus = sum((n_gpus for process_on_nodes in self.resource_pool_spec.values() for n_gpus in process_on_nodes))
        while time.time() - start_time < timeout:
            node_available_resources = ray.state.available_resources_per_node()
            node_available_gpus = {node: node_info.get('GPU', 0) if 'GPU' in node_info else node_info.get('NPU', 0) for node, node_info in node_available_resources.items()}
            total_available_gpus = sum(node_available_gpus.values())
            if total_available_gpus >= total_required_gpus:
                logger.success(f'Total required GPUs ({total_required_gpus}) are available. Verifying placement possibility.')
                try:
                    self._verify_placement_possible(node_available_gpus.copy())
                    logger.success('All resource pools can be satisfied. Proceeding.')
                    return
                except ValueError as e:
                    logger.error(f'Placement check failed: {e}')
                    raise
            logger.info(f'Waiting for nodes... Available GPUs: {total_available_gpus}/{total_required_gpus}. Retrying in {interval} seconds...')
            time.sleep(interval)
        final_available_gpus = sum((node_info.get('GPU', 0) if 'GPU' in node_info else node_info.get('NPU', 0) for node_info in ray.state.available_resources_per_node().values()))
        error_msg = f'Timed out after {timeout} seconds. The cluster does not have enough resources. Required: {total_required_gpus} GPUs, Available: {final_available_gpus} GPUs.'
        logger.error(error_msg)
        raise TimeoutError(error_msg)

    def _verify_placement_possible(self, available_gpus_per_node: dict):
        """
        Checks if each resource pool can be satisfied with the current cluster topology.
        This is a greedy check.

        Args:
            available_gpus_per_node (dict): A copy of the dictionary mapping node ID to its available GPU count.
        """
        sorted_pools = sorted(self.resource_pool_spec.items(), key=lambda item: item[1][0], reverse=True)
        for resource_pool_name, process_on_nodes in sorted_pools:
            num_gpus_per_process, num_nodes = (process_on_nodes[0], len(process_on_nodes))
            found_nodes = 0
            sorted_available_nodes = sorted(available_gpus_per_node.items(), key=lambda item: item[1], reverse=True)
            temp_gpus_per_node = dict(sorted_available_nodes)
            for node, available_gpus in temp_gpus_per_node.items():
                if available_gpus >= num_gpus_per_process:
                    temp_gpus_per_node[node] -= num_gpus_per_process
                    found_nodes += 1
                    if found_nodes == num_nodes:
                        break
            if found_nodes < num_nodes:
                raise ValueError(f"Resource pool '{resource_pool_name}' (requires {num_nodes} nodes with {num_gpus_per_process} GPUs each) cannot be satisfied by the current cluster resource distribution.")
            available_gpus_per_node.update(temp_gpus_per_node)