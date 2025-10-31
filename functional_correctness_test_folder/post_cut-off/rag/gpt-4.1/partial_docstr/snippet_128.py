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
        '''
        Initialize the GraphPartitioner.
        Args:
            build_type: Build type for the executables ("debug" or "release")
        '''
        self.build_type = build_type.lower()
        self._exec_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "diskann_bin", self.build_type)
        self._required_executables = ["graph_partition", "partition_info"]

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        exe_name = name
        if sys.platform == "win32":
            exe_name += ".exe"
        exe_path = os.path.join(self._exec_dir, exe_name)
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(
                f"Executable '{exe_name}' not found at {exe_path}.")
        return exe_path

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        missing = []
        for exe in self._required_executables:
            try:
                self._get_executable_path(exe)
            except FileNotFoundError:
                missing.append(exe)
        if missing:
            self._build_executables()
            # Re-check after build
            for exe in missing:
                self._get_executable_path(exe)

    def _build_executables(self):
        '''Build the required executables.'''
        # Assume CMake-based build in a sibling 'diskann' directory
        root_dir = os.path.dirname(os.path.abspath(__file__))
        diskann_src = os.path.join(root_dir, "diskann")
        build_dir = os.path.join(root_dir, "diskann_bin", self.build_type)
        os.makedirs(build_dir, exist_ok=True)
        cmake_build_type = "Release" if self.build_type == "release" else "Debug"
        cmake_cmd = [
            "cmake",
            "-DCMAKE_BUILD_TYPE=" + cmake_build_type,
            diskann_src
        ]
        build_cmd = ["cmake", "--build", ".", "--config", cmake_build_type]
        try:
            subprocess.check_call(cmake_cmd, cwd=build_dir)
            subprocess.check_call(build_cmd, cwd=build_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to build DiskANN executables: {e}")

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
        self._ensure_executables()
        if not os.path.exists(index_prefix_path + ".index"):
            raise FileNotFoundError(
                f"Index file not found: {index_prefix_path}.index")
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
        exe = self._get_executable_path("graph_partition")
        disk_graph_index_path = os.path.join(
            output_dir, f"{partition_prefix}_disk_graph.index")
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
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Graph partitioning failed: {e.stderr or e.stdout}")
        if not (os.path.isfile(disk_graph_index_path) and os.path.isfile(partition_bin_path)):
            raise RuntimeError(
                "Partitioning did not produce expected output files.")
        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        self._ensure_executables()
        exe = self._get_executable_path("partition_info")
        cmd = [exe, "--partition_bin", partition_bin_path]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            output = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Failed to get partition info: {e.stderr or e.stdout}")
        # Parse output as key: value per line
        info = {}
        for line in output.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # Try to convert to int or float if possible
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except Exception:
                    pass
                info[key] = value
        return info
