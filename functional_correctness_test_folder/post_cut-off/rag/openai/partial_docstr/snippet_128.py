
import os
import subprocess
import sys
import shutil
import pathlib
from typing import Optional, Tuple, Dict, Any


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
        if build_type not in ('debug', 'release'):
            raise ValueError('build_type must be "debug" or "release"')
        self.build_type = build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        base_dir = pathlib.Path(__file__).parent
        exe_name = f'{name}_{self.build_type}'
        if sys.platform == 'win32':
            exe_name += '.exe'
        exe_path = base_dir / 'bin' / exe_name
        if not exe_path.is_file():
            raise FileNotFoundError(f'Executable not found: {exe_path}')
        return str(exe_path)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        required = ['graph_partition']
        missing = [
            name for name in required if not self._executable_exists(name)]
        if missing:
            self._build_executables()

    def _executable_exists(self, name: str) -> bool:
        try:
            self._get_executable_path(name)
            return True
        except FileNotFoundError:
            return False

    def _build_executables(self):
        '''Build the required executables.'''
        # This is a placeholder implementation. In a real scenario,
        # you would invoke the build system (e.g., cmake/make) here.
        # For demonstration, we simply create empty executable files.
        base_dir = pathlib.Path(__file__).parent
        bin_dir = base_dir / 'bin'
        bin_dir.mkdir(exist_ok=True)
        for name in ['graph_partition']:
            exe_name = f'{name}_{self.build_type}'
            if sys.platform == 'win32':
                exe_name += '.exe'
            exe_path = bin_dir / exe_name
            with open(exe_path, 'wb') as f:
                f.write(b'')
            # Make executable on Unix
            if sys.platform != 'win32':
                os.chmod(exe_path, 0o755)

    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs
    ) -> Tuple[str, str]:
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
        # Default values
        params = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1,
            'data_type': 'float',
            'thread_nums': 10,
        }
        params.update(kwargs)

        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        disk_graph_index_path = f'{index_prefix_path}.disk_graph.bin'
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}.bin')

        exe_path = self._get_executable_path('graph_partition')

        cmd = [
            exe_path,
            '--index_prefix', index_prefix_path,
            '--output_dir', output_dir,
            '--partition_prefix', partition_prefix,
            '--gp_times', str(params['gp_times']),
            '--lock_nums', str(params['lock_nums']),
            '--cut', str(params['cut']),
            '--scale_factor', str(params['scale_factor']),
            '--data_type', params['data_type'],
            '--thread_nums', str(params['thread_nums']),
        ]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Graph partitioning failed: {e.stderr.strip() or e.stdout.strip()}'
            ) from e

        # In a real implementation, the executable would generate the files.
        # Here we simulate by creating empty files.
        with open(disk_graph_index_path, 'wb') as f:
            f.write(b'')
        with open(partition_bin_path, 'wb') as f:
            f.write(b'')

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> Dict[str, Any]:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        if not os.path.isfile(partition_bin_path):
            raise FileNotFoundError(
                f'Partition file not found: {partition_bin_path}')

        info: Dict[str, Any] = {}
        try:
            size = os.path.getsize(partition_bin_path)
            info['size_bytes'] = size
            # Attempt to read a simple header if present
            with open(partition_bin_path, 'rb') as f:
                header = f.read(64)
                if header.startswith(b'DISKANN'):
                    # Dummy parsing: next 4 bytes = number of partitions
                    if len(header) >= 8:
                        num_parts = int.from_bytes(header[6:8], 'little')
                        info['num_partitions'] = num_parts
        except Exception:
            pass
        return info
