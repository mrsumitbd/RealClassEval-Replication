
import os
import subprocess
from typing import Optional, Tuple


class GraphPartitioner:

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        return os.path.join(os.path.dirname(__file__), 'bin', self.build_type, name)

    def _ensure_executables(self):
        if not os.path.exists(self._get_executable_path('partition')):
            self._build_executables()

    def _build_executables(self):
        build_dir = os.path.join(os.path.dirname(__file__), 'build')
        os.makedirs(build_dir, exist_ok=True)
        subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=' +
                       self.build_type, '..'], cwd=build_dir, check=True)
        subprocess.run(['make'], cwd=build_dir, check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> Tuple[str, str]:
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        partition_bin_path = os.path.join(
            output_dir, partition_prefix + '.partitionbin')
        partition_info_path = os.path.join(
            output_dir, partition_prefix + '.partitioninfo')

        cmd = [self._get_executable_path(
            'partition'), '-o', partition_bin_path, index_prefix_path]
        for key, value in kwargs.items():
            cmd.extend(['-' + key, str(value)])

        subprocess.run(cmd, check=True)

        return partition_bin_path, partition_info_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        partition_info_path = os.path.splitext(partition_bin_path)[
            0] + '.partitioninfo'
        with open(partition_info_path, 'r') as f:
            lines = f.readlines()

        partition_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                partition_info[key.strip()] = value.strip()

        return partition_info
