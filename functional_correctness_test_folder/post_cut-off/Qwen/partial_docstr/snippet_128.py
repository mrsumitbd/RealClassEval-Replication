
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
        self.executables = {
            'partition': 'diskann_partition'
        }

    def _get_executable_path(self, name: str) -> str:
        return os.path.join('build', self.build_type, self.executables[name])

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        try:
            subprocess.run(
                ['make', f'build_type={self.build_type}'], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to build executables") from e

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
        self._ensure_executables()
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        command = [
            self._get_executable_path('partition'),
            '-index', index_prefix_path,
            '-out', output_dir,
            '-prefix', partition_prefix,
            '-gp_times', str(kwargs.get('gp_times', 10)),
            '-lock_nums', str(kwargs.get('lock_nums', 10)),
            '-cut', str(kwargs.get('cut', 100)),
            '-scale_factor', str(kwargs.get('scale_factor', 1)),
            '-data_type', kwargs.get('data_type', 'float'),
            '-thread_nums', str(kwargs.get('thread_nums', 10))
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Graph partitioning failed") from e

        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk_graph.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")
        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        # Placeholder for actual implementation to read and parse partition file
        # For demonstration, returning a dummy dictionary
        return {
            'file_path': partition_bin_path,
            'num_partitions': 10,
            'partition_size': 1024,
            'data_type': 'float'
        }
