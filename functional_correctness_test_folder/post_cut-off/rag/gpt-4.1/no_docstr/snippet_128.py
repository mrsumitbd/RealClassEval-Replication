import os
import subprocess
import sys
import shutil
import tempfile
import json
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
        self.build_type = build_type.lower()
        self._exec_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'bin', self.build_type)
        self._required_executables = ['graph_partition', 'partition_info']
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        exe_name = name
        if sys.platform == 'win32':
            exe_name += '.exe'
        exe_path = os.path.join(self._exec_dir, exe_name)
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(
                f"Executable '{exe_name}' not found at '{exe_path}'.")
        return exe_path

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        missing = []
        for exe in self._required_executables:
            exe_path = os.path.join(self._exec_dir, exe)
            if sys.platform == 'win32':
                exe_path += '.exe'
            if not os.path.isfile(exe_path):
                missing.append(exe)
        if missing:
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        # Assume CMake-based build in a sibling 'diskann' directory
        root_dir = os.path.dirname(os.path.abspath(__file__))
        diskann_dir = os.path.join(root_dir, 'diskann')
        build_dir = os.path.join(diskann_dir, 'build', self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        cmake_args = ['cmake', '..']
        if self.build_type == 'release':
            cmake_args += ['-DCMAKE_BUILD_TYPE=Release']
        elif self.build_type == 'debug':
            cmake_args += ['-DCMAKE_BUILD_TYPE=Debug']
        else:
            raise ValueError(f"Unknown build_type: {self.build_type}")
        # Run cmake
        subprocess.check_call(cmake_args, cwd=build_dir)
        # Build
        if sys.platform == 'win32':
            build_cmd = ['cmake', '--build', '.',
                         '--config', self.build_type.capitalize()]
        else:
            build_cmd = ['cmake', '--build', '.', '--', '-j4']
        subprocess.check_call(build_cmd, cwd=build_dir)
        # Copy executables to bin directory
        os.makedirs(self._exec_dir, exist_ok=True)
        for exe in self._required_executables:
            if sys.platform == 'win32':
                exe_file = exe + '.exe'
            else:
                exe_file = exe
            src_path = os.path.join(build_dir, exe_file)
            dst_path = os.path.join(self._exec_dir, exe_file)
            if not os.path.isfile(src_path):
                raise FileNotFoundError(
                    f"Built executable '{src_path}' not found after build.")
            shutil.copy2(src_path, dst_path)

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
        if not os.path.exists(index_prefix_path + "_disk.index"):
            raise FileNotFoundError(
                f"DiskANN index file not found: {index_prefix_path}_disk.index")
        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(index_prefix_path))
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)
        os.makedirs(output_dir, exist_ok=True)
        # Default parameters
        params = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1,
            'data_type': 'float',
            'thread_nums': 10
        }
        params.update(kwargs)
        exe_path = self._get_executable_path('graph_partition')
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk_graph.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")
        cmd = [
            exe_path,
            '-i', index_prefix_path,
            '-o', output_dir,
            '-p', partition_prefix,
            '-g', str(params['gp_times']),
            '-l', str(params['lock_nums']),
            '-c', str(params['cut']),
            '-s', str(params['scale_factor']),
            '-d', str(params['data_type']),
            '-t', str(params['thread_nums'])
        ]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Graph partitioning failed: {e.stderr or e.stdout}")
        if not os.path.isfile(disk_graph_index_path):
            raise RuntimeError(
                f"Partitioning did not produce disk graph index: {disk_graph_index_path}")
        if not os.path.isfile(partition_bin_path):
            raise RuntimeError(
                f"Partitioning did not produce partition bin: {partition_bin_path}")
        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        if not os.path.isfile(partition_bin_path):
            raise FileNotFoundError(
                f"Partition file not found: {partition_bin_path}")
        exe_path = self._get_executable_path('partition_info')
        with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.json') as tmpf:
            tmp_json = tmpf.name
        cmd = [
            exe_path,
            '-i', partition_bin_path,
            '-j', tmp_json
        ]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            os.remove(tmp_json)
            raise RuntimeError(
                f"Partition info failed: {e.stderr or e.stdout}")
        try:
            with open(tmp_json, 'r') as f:
                info = json.load(f)
        finally:
            os.remove(tmp_json)
        return info
