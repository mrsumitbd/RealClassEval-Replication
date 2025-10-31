
import os
import subprocess
import shutil
import sys
from typing import Optional


class GraphPartitioner:
    '''
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    '''

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type.lower()
        self._exec_names = {
            'partition': 'graph_partition',
            'info': 'partition_info'
        }
        self._bin_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'bin', self.build_type)
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        exe = self._exec_names.get(name)
        if not exe:
            raise ValueError(f"Unknown executable name: {name}")
        if sys.platform == "win32":
            exe += ".exe"
        return os.path.join(self._bin_dir, exe)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        for name in self._exec_names:
            exe_path = self._get_executable_path(name)
            if not os.path.isfile(exe_path):
                self._build_executables()
                break

    def _build_executables(self):
        '''Build the required executables.'''
        src_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(src_dir, 'build', self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        cmake_cmd = [
            'cmake',
            '-DCMAKE_BUILD_TYPE={}'.format(self.build_type.capitalize()),
            src_dir
        ]
        build_cmd = ['cmake', '--build', '.',
                     '--config', self.build_type.capitalize()]
        try:
            subprocess.check_call(cmake_cmd, cwd=build_dir)
            subprocess.check_call(build_cmd, cwd=build_dir)
            # Copy executables to bin dir
            os.makedirs(self._bin_dir, exist_ok=True)
            for name in self._exec_names:
                exe_name = self._exec_names[name]
                if sys.platform == "win32":
                    exe_name += ".exe"
                src_exe = os.path.join(build_dir, exe_name)
                if not os.path.isfile(src_exe):
                    # Try in build_dir/{Release,Debug}
                    alt_dir = os.path.join(
                        build_dir, self.build_type.capitalize())
                    src_exe = os.path.join(alt_dir, exe_name)
                if not os.path.isfile(src_exe):
                    raise RuntimeError(f"Failed to build {exe_name}")
                shutil.copy2(src_exe, self._get_executable_path(name))
        except Exception as e:
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
        if not os.path.exists(index_prefix_path + ".index"):
            raise FileNotFoundError(
                f"Index file not found: {index_prefix_path}.index")
        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(index_prefix_path))
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)
        os.makedirs(output_dir, exist_ok=True)

        params = {
            'gp_times': kwargs.get('gp_times', 10),
            'lock_nums': kwargs.get('lock_nums', 10),
            'cut': kwargs.get('cut', 100),
            'scale_factor': kwargs.get('scale_factor', 1),
            'data_type': kwargs.get('data_type', 'float'),
            'thread_nums': kwargs.get('thread_nums', 10)
        }

        exe_path = self._get_executable_path('partition')
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")

        cmd = [
            exe_path,
            "--index_prefix", index_prefix_path,
            "--output_dir", output_dir,
            "--partition_prefix", partition_prefix,
            "--gp_times", str(params['gp_times']),
            "--lock_nums", str(params['lock_nums']),
            "--cut", str(params['cut']),
            "--scale_factor", str(params['scale_factor']),
            "--data_type", str(params['data_type']),
            "--thread_nums", str(params['thread_nums'])
        ]

        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Partitioning failed: {e.stderr.strip()}")

        if not os.path.isfile(disk_graph_index_path):
            raise RuntimeError(
                f"Partitioning failed: {disk_graph_index_path} not found")
        if not os.path.isfile(partition_bin_path):
            raise RuntimeError(
                f"Partitioning failed: {partition_bin_path} not found")

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
        exe_path = self._get_executable_path('info')
        cmd = [exe_path, "--partition_bin", partition_bin_path, "--json"]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding='utf-8')
            import json
            info = json.loads(result.stdout)
            return info
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Failed to get partition info: {e.stderr.strip()}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse partition info: {e}")
