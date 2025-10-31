
import subprocess
import os
from typing import Optional, Dict, Tuple


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
        return os.path.join(os.path.dirname(__file__), f'{name}_{self.build_type}')

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('graph_partitioner')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        # Assuming the build process is done using a Makefile in the same directory
        subprocess.run(['make', f'BUILD_TYPE={self.build_type}'], cwd=os.path.dirname(
            __file__), check=True)

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

        executable_path = self._get_executable_path('graph_partitioner')
        command = [executable_path, '--index_prefix_path', index_prefix_path,
                   '--output_dir', output_dir, '--partition_prefix', partition_prefix]

        gp_times = kwargs.get('gp_times', 10)
        lock_nums = kwargs.get('lock_nums', 10)
        cut = kwargs.get('cut', 100)
        scale_factor = kwargs.get('scale_factor', 1)
        data_type = kwargs.get('data_type', 'float')
        thread_nums = kwargs.get('thread_nums', 10)

        command.extend(['--gp_times', str(gp_times), '--lock_nums', str(lock_nums), '--cut', str(cut),
                       '--scale_factor', str(scale_factor), '--data_type', data_type, '--thread_nums', str(thread_nums)])

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Graph partitioning failed with error code {e.returncode}') from e

        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}.diskann')
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}.partition.bin')

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> Dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        # Assuming there's an executable to get partition info
        executable_path = self._get_executable_path('partition_info')
        command = [executable_path, '--partition_bin_path', partition_bin_path]

        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Failed to get partition info with error code {e.returncode}') from e

        # Assuming the output is in a simple key-value format, e.g., "key1=value1\nkey2=value2"
        info = {}
        for line in output.decode('utf-8').splitlines():
            key, value = line.split('=')
            info[key.strip()] = value.strip()

        return info
