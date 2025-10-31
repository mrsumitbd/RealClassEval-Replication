
import os
import subprocess
from typing import Optional, Dict, Any


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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(script_dir, 'build', self.build_type)
        return os.path.join(build_dir, name)

    def _ensure_executables(self):
        required_executables = ['partition_graph']
        for exe in required_executables:
            if not os.path.exists(self._get_executable_path(exe)):
                self._build_executables()
                break

    def _build_executables(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(script_dir, 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=' +
                       self.build_type, '..'], cwd=build_dir, check=True)
        subprocess.run(['make', 'partition_graph'], cwd=build_dir, check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> tuple[str, str]:
        default_kwargs = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1,
            'data_type': 'float',
            'thread_nums': 10
        }
        params = {**default_kwargs, **kwargs}

        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        cmd = [
            self._get_executable_path('partition_graph'),
            index_prefix_path,
            output_dir,
            partition_prefix,
            str(params['gp_times']),
            str(params['lock_nums']),
            str(params['cut']),
            str(params['scale_factor']),
            params['data_type'],
            str(params['thread_nums'])
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Partitioning failed: {result.stderr}")

        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}.disk.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}.partition.bin")

        return (disk_graph_index_path, partition_bin_path)

    def get_partition_info(self, partition_bin_path: str) -> dict:
        if not os.path.exists(partition_bin_path):
            raise RuntimeError(
                f"Partition file not found: {partition_bin_path}")

        cmd = [
            self._get_executable_path('partition_graph'),
            '--info',
            partition_bin_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to get partition info: {result.stderr}")

        info = {}
        for line in result.stdout.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()

        return info
