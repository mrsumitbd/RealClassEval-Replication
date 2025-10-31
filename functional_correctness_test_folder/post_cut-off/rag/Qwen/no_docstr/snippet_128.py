
import os
import subprocess
from typing import Optional, Dict


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
        self.executables_dir = os.path.join(
            os.path.dirname(__file__), 'executables', build_type)

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        return os.path.join(self.executables_dir, name)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self.executables_dir) or not os.listdir(self.executables_dir):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        build_script = os.path.join(os.path.dirname(__file__), 'build.sh')
        subprocess.run([build_script, self.build_type], check=True)

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
        partition_executable = self._get_executable_path('partition_graph')
        output_dir = output_dir or os.path.dirname(index_prefix_path)
        partition_prefix = partition_prefix or os.path.basename(
            index_prefix_path)
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}.bin')
        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}_disk_graph.index')

        args = [
            partition_executable,
            '--index_prefix_path', index_prefix_path,
            '--output_dir', output_dir,
            '--partition_prefix', partition_prefix,
            '--gp_times', str(kwargs.get('gp_times', 10)),
            '--lock_nums', str(kwargs.get('lock_nums', 10)),
            '--cut', str(kwargs.get('cut', 100)),
            '--scale_factor', str(kwargs.get('scale_factor', 1)),
            '--data_type', kwargs.get('data_type', 'float'),
            '--thread_nums', str(kwargs.get('thread_nums', 10))
        ]

        result = subprocess.run(args, capture_output=True, text=True)
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
        info_executable = self._get_executable_path('partition_info')
        result = subprocess.run(
            [info_executable, partition_bin_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to get partition info: {result.stderr}")

        info_lines = result.stdout.strip().split('\n')
        partition_info = {}
        for line in info_lines:
            key, value = line.split(': ')
            partition_info[key] = value

        return partition_info
