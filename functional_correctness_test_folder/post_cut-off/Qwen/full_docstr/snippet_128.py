
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
        '''
        Initialize the GraphPartitioner.
        Args:
            build_type: Build type for the executables ("debug" or "release")
        '''
        self.build_type = build_type
        self.executables = {
            'partition': 'diskann_partition'
        }

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        return os.path.join('build', self.build_type, self.executables[name])

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        try:
            subprocess.run(['make', self.build_type], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build executables: {e}")

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
        output_dir = output_dir or os.path.dirname(index_prefix_path)
        partition_prefix = partition_prefix or os.path.basename(
            index_prefix_path)
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk_graph.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")

        args = [
            self._get_executable_path('partition'),
            '-index', index_prefix_path,
            '-output', output_dir,
            '-prefix', partition_prefix,
            '-gp_times', str(kwargs.get('gp_times', 10)),
            '-lock_nums', str(kwargs.get('lock_nums', 10)),
            '-cut', str(kwargs.get('cut', 100)),
            '-scale_factor', str(kwargs.get('scale_factor', 1)),
            '-data_type', kwargs.get('data_type', 'float'),
            '-thread_nums', str(kwargs.get('thread_nums', 10))
        ]

        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Graph partitioning failed: {e}")

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        # Placeholder for actual implementation to read partition info
        # This is a mock implementation and should be replaced with actual file reading logic
        return {
            'file_path': partition_bin_path,
            'size': os.path.getsize(partition_bin_path),
            'status': 'active'
        }
