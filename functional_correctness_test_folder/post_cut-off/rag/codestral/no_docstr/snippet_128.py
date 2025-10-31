
import os
import subprocess
from typing import Optional, Tuple


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
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        return os.path.join(os.path.dirname(__file__), 'build', self.build_type, name)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('build_graph_partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        build_dir = os.path.join(os.path.dirname(
            __file__), 'build', self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        subprocess.run(['cmake', '-S', os.path.dirname(__file__), '-B',
                       build_dir, f'-DCMAKE_BUILD_TYPE={self.build_type}'], check=True)
        subprocess.run(['cmake', '--build', build_dir,
                       '--target', 'build_graph_partition'], check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> Tuple[str, str]:
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

        gp_times = kwargs.get('gp_times', 10)
        lock_nums = kwargs.get('lock_nums', 10)
        cut = kwargs.get('cut', 100)
        scale_factor = kwargs.get('scale_factor', 1)
        data_type = kwargs.get('data_type', 'float')
        thread_nums = kwargs.get('thread_nums', 10)

        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}_disk_graph_index')
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}_partition.bin')

        cmd = [
            self._get_executable_path('build_graph_partition'),
            '-input', index_prefix_path,
            '-output', disk_graph_index_path,
            '-partition', partition_bin_path,
            '-gp_times', str(gp_times),
            '-lock_nums', str(lock_nums),
            '-cut', str(cut),
            '-scale_factor', str(scale_factor),
            '-data_type', data_type,
            '-thread_nums', str(thread_nums)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f'Graph partitioning failed: {result.stderr}')

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        if not os.path.exists(partition_bin_path):
            raise FileNotFoundError(
                f'Partition file not found: {partition_bin_path}')

        with open(partition_bin_path, 'rb') as f:
            # Read header information (first 4 bytes for number of partitions)
            num_partitions = int.from_bytes(f.read(4), byteorder='little')

            # Read partition sizes (next num_partitions * 4 bytes)
            partition_sizes = []
            for _ in range(num_partitions):
                partition_sizes.append(int.from_bytes(
                    f.read(4), byteorder='little'))

            return {
                'num_partitions': num_partitions,
                'partition_sizes': partition_sizes,
                'total_nodes': sum(partition_sizes)
            }
