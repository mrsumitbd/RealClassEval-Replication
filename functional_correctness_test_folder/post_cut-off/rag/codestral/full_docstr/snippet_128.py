
import os
import subprocess
from typing import Optional, Dict, Any
import shutil


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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(script_dir, '..', 'build', self.build_type)
        return os.path.join(build_dir, name)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        if not os.path.exists(self._get_executable_path('partition')):
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(script_dir, '..', 'build', self.build_type)
        os.makedirs(build_dir, exist_ok=True)

        cmake_cmd = [
            'cmake',
            '-S', os.path.join(script_dir, '..'),
            '-B', build_dir,
            f'-DCMAKE_BUILD_TYPE={self.build_type.upper()}'
        ]
        subprocess.run(cmake_cmd, check=True)

        build_cmd = [
            'cmake',
            '--build', build_dir,
            '--target', 'partition'
        ]
        subprocess.run(build_cmd, check=True)

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

        os.makedirs(output_dir, exist_ok=True)

        partition_exe = self._get_executable_path('partition')

        cmd = [
            partition_exe,
            '-i', index_prefix_path,
            '-o', output_dir,
            '-p', partition_prefix,
            '--gp_times', str(kwargs.get('gp_times', 10)),
            '--lock_nums', str(kwargs.get('lock_nums', 10)),
            '--cut', str(kwargs.get('cut', 100)),
            '--scale_factor', str(kwargs.get('scale_factor', 1)),
            '--data_type', kwargs.get('data_type', 'float'),
            '--thread_nums', str(kwargs.get('thread_nums', 10))
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Partitioning failed: {result.stderr}")

        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk.index")
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
        if not os.path.exists(partition_bin_path):
            raise FileNotFoundError(
                f"Partition file not found: {partition_bin_path}")

        # Read the partition file header to get basic information
        with open(partition_bin_path, 'rb') as f:
            # Read the first 4 bytes to get the number of partitions
            num_partitions = int.from_bytes(f.read(4), byteorder='little')

            # Read the next 4 bytes to get the number of nodes
            num_nodes = int.from_bytes(f.read(4), byteorder='little')

            # Read the next 4 bytes to get the number of edges
            num_edges = int.from_bytes(f.read(4), byteorder='little')

        return {
            'num_partitions': num_partitions,
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'file_size': os.path.getsize(partition_bin_path)
        }
