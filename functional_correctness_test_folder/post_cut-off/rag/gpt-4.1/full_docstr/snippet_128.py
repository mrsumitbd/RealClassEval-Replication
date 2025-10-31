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
        self._executables = {
            "graph_partition": "graph_partition",
            "partition_info": "partition_info"
        }
        self._bin_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "bin", self.build_type)
        self._src_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "diskann", "tools")
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        exe = self._executables.get(name)
        if not exe:
            raise ValueError(f"Unknown executable: {name}")
        exe_path = os.path.join(self._bin_dir, exe)
        if sys.platform == "win32":
            exe_path += ".exe"
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"Executable not found: {exe_path}")
        return exe_path

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        for exe in self._executables.values():
            exe_path = os.path.join(self._bin_dir, exe)
            if sys.platform == "win32":
                exe_path += ".exe"
            if not os.path.isfile(exe_path):
                self._build_executables()
                break

    def _build_executables(self):
        '''Build the required executables.'''
        # Assume CMake-based build in diskann/tools
        build_dir = os.path.join(
            self._bin_dir, "..", "build_" + self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        cmake_args = [
            "cmake",
            self._src_dir,
            f"-DCMAKE_BUILD_TYPE={self.build_type.capitalize()}",
            f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY={self._bin_dir}"
        ]
        build_args = ["cmake", "--build", ".",
                      "--config", self.build_type.capitalize()]
        try:
            subprocess.check_call(cmake_args, cwd=build_dir)
            subprocess.check_call(build_args, cwd=build_dir)
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
        exe = self._get_executable_path("graph_partition")
        if not os.path.isfile(index_prefix_path + "_disk.index"):
            raise FileNotFoundError(
                f"DiskANN index not found: {index_prefix_path}_disk.index")
        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(index_prefix_path))
        os.makedirs(output_dir, exist_ok=True)
        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)
        # Default parameters
        params = {
            "gp_times": kwargs.get("gp_times", 10),
            "lock_nums": kwargs.get("lock_nums", 10),
            "cut": kwargs.get("cut", 100),
            "scale_factor": kwargs.get("scale_factor", 1),
            "data_type": kwargs.get("data_type", "float"),
            "thread_nums": kwargs.get("thread_nums", 10)
        }
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk.index")
        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}_partition.bin")
        cmd = [
            exe,
            "--index_prefix", index_prefix_path,
            "--output_dir", output_dir,
            "--partition_prefix", partition_prefix,
            "--gp_times", str(params["gp_times"]),
            "--lock_nums", str(params["lock_nums"]),
            "--cut", str(params["cut"]),
            "--scale_factor", str(params["scale_factor"]),
            "--data_type", str(params["data_type"]),
            "--thread_nums", str(params["thread_nums"])
        ]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding="utf-8")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Graph partitioning failed: {e.stderr or e.stdout}")
        if not os.path.isfile(disk_graph_index_path):
            raise RuntimeError(
                f"Partitioned disk index not found: {disk_graph_index_path}")
        if not os.path.isfile(partition_bin_path):
            raise RuntimeError(
                f"Partition bin not found: {partition_bin_path}")
        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        exe = self._get_executable_path("partition_info")
        if not os.path.isfile(partition_bin_path):
            raise FileNotFoundError(
                f"Partition bin not found: {partition_bin_path}")
        cmd = [exe, "--partition_bin", partition_bin_path, "--json"]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding="utf-8")
            output = result.stdout.strip()
            info = json.loads(output)
            return info
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Partition info failed: {e.stderr or e.stdout}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse partition info: {e}")
