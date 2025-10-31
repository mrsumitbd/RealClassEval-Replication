
import os
import subprocess
from typing import Optional
import shutil


class GraphPartitioner:

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self.executables = ['metis_partitioner', 'partition_info']
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        return os.path.join(os.path.dirname(__file__), 'build', self.build_type, name)

    def _ensure_executables(self):
        for executable in self.executables:
            executable_path = self._get_executable_path(executable)
            if not os.path.exists(executable_path):
                self._build_executables()
                break

    def _build_executables(self):
        build_dir = os.path.join(os.path.dirname(__file__), 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=' +
                       self.build_type, '..'], cwd=build_dir)
        subprocess.run(['cmake', '--build', '.'], cwd=build_dir)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> tuple[str, str]:
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if partition_prefix is None:
            partition_prefix = os.path.basename(
                index_prefix_path) + '_partition'

        partition_bin_path = os.path.join(
            output_dir, partition_prefix + '.bin')
        partition_txt_path = os.path.join(
            output_dir, partition_prefix + '.txt')

        executable_path = self._get_executable_path('metis_partitioner')
        command = [executable_path, index_prefix_path, partition_bin_path]
        for key, value in kwargs.items():
            command.extend([f'--{key}', str(value)])
        subprocess.run(command)

        return partition_bin_path, partition_txt_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        executable_path = self._get_executable_path('partition_info')
        output = subprocess.check_output(
            [executable_path, partition_bin_path]).decode('utf-8')
        info = {}
        for line in output.splitlines():
            key, value = line.split(':')
            info[key.strip()] = int(value.strip())
        return info
