
import os
import subprocess
from typing import Optional


class GraphPartitioner:
    '''
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    '''

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        return os.path.join(os.path.dirname(__file__), 'build', self.build_type, name)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        build_dir = os.path.join(os.path.dirname(
            __file__), 'build', self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        subprocess.run(['cmake', '-B', build_dir,
                       '-DCMAKE_BUILD_TYPE=' + self.build_type, '..'], check=True)
        subprocess.run(['cmake', '--build', build_dir,
                       '--target', 'partition'], check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> tuple[str, str]:
        '''
        Partition a disk-based index for improved performance.
        Args:
            index_prefix_path: Path to the index prefix (e.g., "/path/to/index")
            output_dir: Output directory for results (defaults to parent of index_prefix_path)
            partition_prefix: Prefix for output files (defaults to basename of index_prefix_path)
            **kwargs: Additional parameters for graph partitioning:
                - gp_times: Number of LDG partition iterations (default: 10)
                - lock_nums: Number of lock nodes (default: 10)
                - cut: Cut adjacency list degree (default: 100)
                - scale_factor: Scale factor (default: 1)
                - data_type: Data type (default: "float")
                - thread_nums: Number of threads (default: 10)
        Returns:
            Tuple of (disk_graph_index_path, partition_bin_path)
        Raises:
            RuntimeError: If the partitioning process fails
        '''
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk_graph_index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")

        cmd = [
            self._get_executable_path('partition'),
            '--input', index_prefix_path,
            '--output', disk_graph_index_path,
            '--partition_prefix', partition_prefix,
            '--output_dir', output_dir,
        ]

        for key, value in kwargs.items():
            cmd.extend([f'--{key}', str(value)])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Partitioning failed: {result.stderr}")

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        with open(partition_bin_path, 'rb') as f:
            data = f.read()

        # Assuming the partition file has a specific binary format
        # This is a placeholder for the actual parsing logic
        partition_info = {
            'num_partitions': int.from_bytes(data[:4], byteorder='little'),
            'partition_sizes': [int.from_bytes(data[4+i*4:8+i*4], byteorder='little') for i in range(int.from_bytes(data[:4], byteorder='little'))],
        }

        return partition_info
