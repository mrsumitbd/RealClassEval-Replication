
import os
import subprocess
from typing import Optional
import struct


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
        if not os.path.exists(self._get_executable_path('graph_partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        subprocess.run(
            ['mkdir', '-p', os.path.join(os.path.dirname(__file__), 'build')])
        subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=' + self.build_type,
                       '..'], cwd=os.path.join(os.path.dirname(__file__), 'build'))
        subprocess.run(['cmake', '--build', '.'],
                       cwd=os.path.join(os.path.dirname(__file__), 'build'))

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

        command = [self._get_executable_path('graph_partition')]
        command.extend(['--index_prefix_path', index_prefix_path])
        command.extend(['--output_dir', output_dir])
        command.extend(['--partition_prefix', partition_prefix])

        for key, value in kwargs.items():
            command.extend(['--' + key, str(value)])

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('Graph partitioning failed') from e

        disk_graph_index_path = os.path.join(
            output_dir, partition_prefix + '_disk_index.graph')
        partition_bin_path = os.path.join(
            output_dir, partition_prefix + '_partition.bin')

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
            num_nodes = struct.unpack('i', f.read(4))[0]
            partition_ids = struct.unpack(
                'i' * num_nodes, f.read(4 * num_nodes))

        partition_info = {
            'num_nodes': num_nodes,
            'partition_ids': partition_ids
        }

        return partition_info
