
import os
import shutil
import subprocess
from typing import Optional


class GraphPartitioner:

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self.exec_names = {
            'partition': 'graph_partitioner',
            'info': 'partition_info'
        }
        self.exec_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'bin', self.build_type)
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        if name not in self.exec_names:
            raise ValueError(f"Unknown executable name: {name}")
        path = os.path.join(self.exec_dir, self.exec_names[name])
        if os.name == 'nt':
            path += '.exe'
        return path

    def _ensure_executables(self):
        for name in self.exec_names:
            path = self._get_executable_path(name)
            if not os.path.isfile(path) or not os.access(path, os.X_OK):
                self._build_executables()
                break

    def _build_executables(self):
        build_script = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'build.sh')
        if not os.path.isfile(build_script):
            raise FileNotFoundError("Build script not found: build.sh")
        result = subprocess.run(
            ['bash', build_script, self.build_type], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Build failed: {result.stderr}")

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> tuple[str, str]:
        partition_exec = self._get_executable_path('partition')
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        if partition_prefix is None:
            partition_prefix = os.path.join(output_dir, 'partition')
        args = [partition_exec, '--index',
                index_prefix_path, '--out', partition_prefix]
        for k, v in kwargs.items():
            if len(k) == 1:
                args.append(f'-{k}')
            else:
                args.append(f'--{k.replace("_", "-")}')
            if v is not None:
                args.append(str(v))
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Partitioning failed: {result.stderr}")
        partition_bin = partition_prefix + '.bin'
        partition_meta = partition_prefix + '.meta'
        if not os.path.isfile(partition_bin) or not os.path.isfile(partition_meta):
            raise FileNotFoundError("Partition output files not found.")
        return partition_bin, partition_meta

    def get_partition_info(self, partition_bin_path: str) -> dict:
        info_exec = self._get_executable_path('info')
        args = [info_exec, '--input', partition_bin_path, '--json']
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Partition info failed: {result.stderr}")
        import json
        return json.loads(result.stdout)
