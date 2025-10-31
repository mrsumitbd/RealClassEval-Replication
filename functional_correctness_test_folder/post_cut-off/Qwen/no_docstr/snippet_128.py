
from typing import Optional
import os
import subprocess


class GraphPartitioner:

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self.executables = {
            'partitioner': 'partitioner_executable'
        }
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        return os.path.join('bin', self.build_type, self.executables[name])

    def _ensure_executables(self):
        for executable in self.executables.values():
            path = self._get_executable_path(executable)
            if not os.path.exists(path):
                self._build_executables()
                break

    def _build_executables(self):
        build_command = f"make -C src BUILD_TYPE={self.build_type}"
        subprocess.run(build_command, shell=True, check=True)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> tuple[str, str]:
        if output_dir is None:
            output_dir = 'output'
        if partition_prefix is None:
            partition_prefix = 'partition'

        os.makedirs(output_dir, exist_ok=True)
        partitioner_path = self._get_executable_path('partitioner')
        output_path = os.path.join(output_dir, partition_prefix)

        command = f"{partitioner_path} --index-prefix {index_prefix_path} --output-prefix {output_path}"
        subprocess.run(command, shell=True, check=True)

        return output_path + '_0.bin', output_path + '_0.meta'

    def get_partition_info(self, partition_bin_path: str) -> dict:
        info = {}
        with open(partition_bin_path.replace('.bin', '.meta'), 'r') as meta_file:
            for line in meta_file:
                key, value = line.strip().split(': ')
                info[key] = value
        return info
