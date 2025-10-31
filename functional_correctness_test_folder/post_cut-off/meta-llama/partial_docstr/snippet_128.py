
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
        self.build_type = build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        current_dir = os.path.dirname(__file__)
        executable_path = os.path.join(
            current_dir, 'build', self.build_type, name)
        return executable_path

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('graph_partitioner')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        current_dir = os.path.dirname(__file__)
        subprocess.run(['mkdir', '-p', os.path.join(current_dir, 'build')])
        subprocess.run(['cmake', '-B', os.path.join(current_dir, 'build'),
                       '-DCMAKE_BUILD_TYPE=' + self.build_type], cwd=current_dir)
        subprocess.run(
            ['cmake', '--build', os.path.join(current_dir, 'build')], cwd=current_dir)

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

        executable_path = self._get_executable_path('graph_partitioner')
        command = [executable_path, index_prefix_path,
                   output_dir, partition_prefix]

        gp_times = kwargs.get('gp_times', 10)
        lock_nums = kwargs.get('lock_nums', 10)
        cut = kwargs.get('cut', 100)
        scale_factor = kwargs.get('scale_factor', 1)
        data_type = kwargs.get('data_type', 'float')
        thread_nums = kwargs.get('thread_nums', 10)

        command.extend(['--gp_times', str(gp_times)])
        command.extend(['--lock_nums', str(lock_nums)])
        command.extend(['--cut', str(cut)])
        command.extend(['--scale_factor', str(scale_factor)])
        command.extend(['--data_type', data_type])
        command.extend(['--thread_nums', str(thread_nums)])

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Partitioning process failed with return code {e.returncode}')

        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}_disk_index.graph')
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}_partition.bin')

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
            partition_ids = [struct.unpack('i', f.read(4))[0]
                             for _ in range(num_nodes)]

        partition_info = {
            'num_nodes': num_nodes,
            'num_partitions': max(partition_ids) + 1,
            'partition_ids': partition_ids
        }

        return partition_info
