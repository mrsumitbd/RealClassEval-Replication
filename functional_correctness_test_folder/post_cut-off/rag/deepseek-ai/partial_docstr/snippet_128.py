
import os
import subprocess
import shutil
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
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        return os.path.join(os.path.dirname(__file__), '..', 'build', self.build_type, 'tools', name)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        required_executables = ['partition_graph', 'get_partition_info']
        for exe in required_executables:
            if not os.path.exists(self._get_executable_path(exe)):
                self._build_executables()
                break

    def _build_executables(self):
        '''Build the required executables.'''
        build_dir = os.path.join(os.path.dirname(__file__), '..', 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.run(['cmake', '..', '-DCMAKE_BUILD_TYPE=' +
                       self.build_type], cwd=build_dir, check=True)
        subprocess.run(['make', '-j', 'partition_graph',
                       'get_partition_info'], cwd=build_dir, check=True)

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

        params = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1,
            'data_type': 'float',
            'thread_nums': 10
        }
        params.update(kwargs)

        cmd = [
            self._get_executable_path('partition_graph'),
            '--data_path', index_prefix_path,
            '--output_dir', output_dir,
            '--prefix', partition_prefix,
            '--gp_times', str(params['gp_times']),
            '--lock_nums', str(params['lock_nums']),
            '--cut', str(params['cut']),
            '--scale_factor', str(params['scale_factor']),
            '--data_type', params['data_type'],
            '--thread_nums', str(params['thread_nums'])
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Graph partitioning failed: {e}")

        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}.disk.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}.partition.bin")

        return (disk_graph_index_path, partition_bin_path)

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        cmd = [
            self._get_executable_path('get_partition_info'),
            '--partition_path', partition_bin_path
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)
            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get partition info: {e}")
