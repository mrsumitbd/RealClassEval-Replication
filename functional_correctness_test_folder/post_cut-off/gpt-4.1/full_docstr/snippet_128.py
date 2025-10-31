
import os
import subprocess
import shutil
import sys
import tempfile
import json
from typing import Optional


class GraphPartitioner:
    '''
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    '''

    _EXECUTABLES = {
        "graph_partition": "graph_partition",
        "partition_info": "partition_info"
    }

    def __init__(self, build_type: str = 'release'):
        '''
        Initialize the GraphPartitioner.
        Args:
            build_type: Build type for the executables ("debug" or "release")
        '''
        self.build_type = build_type.lower()
        if self.build_type not in ("debug", "release"):
            raise ValueError("build_type must be 'debug' or 'release'")
        self._diskann_root = os.environ.get(
            "DISKANN_ROOT", os.path.abspath(os.path.dirname(__file__)))
        self._bin_dir = os.path.join(
            self._diskann_root, "build", self.build_type, "bin")
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        exe_name = self._EXECUTABLES.get(name)
        if exe_name is None:
            raise ValueError(f"Unknown executable: {name}")
        exe_path = os.path.join(self._bin_dir, exe_name)
        if sys.platform == "win32":
            exe_path += ".exe"
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"Executable not found: {exe_path}")
        return exe_path

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        missing = []
        for exe in self._EXECUTABLES:
            try:
                self._get_executable_path(exe)
            except FileNotFoundError:
                missing.append(exe)
        if missing:
            self._build_executables()
            # Re-check
            for exe in missing:
                self._get_executable_path(exe)

    def _build_executables(self):
        '''Build the required executables.'''
        build_dir = os.path.join(self._diskann_root, "build", self.build_type)
        if not os.path.isdir(build_dir):
            os.makedirs(build_dir, exist_ok=True)
        cmake_cmd = [
            "cmake",
            "-DCMAKE_BUILD_TYPE={}".format(self.build_type.capitalize()),
            "../.."
        ]
        make_cmd = ["cmake", "--build", ".",
                    "--config", self.build_type.capitalize()]
        try:
            subprocess.check_call(cmake_cmd, cwd=build_dir)
            subprocess.check_call(make_cmd, cwd=build_dir)
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
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        # Default parameters
        params = {
            "gp_times": 10,
            "lock_nums": 10,
            "cut": 100,
            "scale_factor": 1,
            "data_type": "float",
            "thread_nums": 10
        }
        params.update(kwargs)

        exe_path = self._get_executable_path("graph_partition")
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")

        cmd = [
            exe_path,
            "--index_prefix", index_prefix_path,
            "--output_dir", output_dir,
            "--partition_prefix", partition_prefix,
            "--gp_times", str(params["gp_times"]),
            "--lock_nums", str(params["lock_nums"]),
            "--cut", str(params["cut"]),
            "--scale_factor", str(params["scale_factor"]),
            "--data_type", params["data_type"],
            "--thread_nums", str(params["thread_nums"])
        ]

        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding="utf-8")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Partitioning failed: {e.stderr.strip() or e.stdout.strip()}")
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
        exe_path = self._get_executable_path("partition_info")
        cmd = [exe_path, "--partition_bin", partition_bin_path, "--json"]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding="utf-8")
            output = result.stdout.strip()
            info = json.loads(output)
            return info
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Failed to get partition info: {e.stderr.strip() or e.stdout.strip()}")
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Partition info output is not valid JSON: {output}")
