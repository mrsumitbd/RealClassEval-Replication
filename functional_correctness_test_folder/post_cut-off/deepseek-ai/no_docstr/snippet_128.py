
import os
import subprocess
from typing import Optional, Tuple


class GraphPartitioner:

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self._executables = {
            'partition_graph': 'partition_graph',
            'get_partition_info': 'get_partition_info'
        }
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        if name not in self._executables:
            raise ValueError(f"Unknown executable: {name}")
        return os.path.join(os.path.dirname(__file__), 'bin', self.build_type, self._executables[name])

    def _ensure_executables(self):
        for name in self._executables:
            path = self._get_executable_path(name)
            if not os.path.exists(path):
                self._build_executables()
                break

    def _build_executables(self):
        build_dir = os.path.join(os.path.dirname(__file__), 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.run(['cmake', '..', '-DCMAKE_BUILD_TYPE=' +
                       self.build_type], cwd=build_dir, check=True)
        subprocess.run(['make', '-j'], cwd=build_dir, check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> Tuple[str, str]:
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(
                index_prefix_path) + '_partition'

        args = [
            self._get_executable_path('partition_graph'),
            '--index_prefix', index_prefix_path,
            '--output_dir', output_dir,
            '--partition_prefix', partition_prefix
        ]

        for key, value in kwargs.items():
            args.extend([f'--{key}', str(value)])

        subprocess.run(args, check=True)

        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}.bin")
        partition_info_path = os.path.join(
            output_dir, f"{partition_prefix}_info.txt")

        return partition_bin_path, partition_info_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        args = [
            self._get_executable_path('get_partition_info'),
            '--partition_bin', partition_bin_path
        ]

        result = subprocess.run(
            args, capture_output=True, text=True, check=True)
        info = {}
        for line in result.stdout.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        return info
