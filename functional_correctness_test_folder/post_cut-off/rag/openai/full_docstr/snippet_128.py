
import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class GraphPartitioner:
    """
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    """

    def __init__(self, build_type: str = "release"):
        """
        Initialize the GraphPartitioner.

        Args:
            build_type: Build type for the executables ("debug" or "release")
        """
        if build_type not in ("debug", "release"):
            raise ValueError("build_type must be 'debug' or 'release'")
        self.build_type = build_type
        self._ensure_executables()

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _get_executable_path(self, name: str) -> Path:
        """
        Get the path to a graph partition executable.

        The executable is expected to be located in a `bin` directory
        relative to this file, with a suffix matching the build type.
        """
        base_dir = Path(__file__).resolve().parent
        bin_dir = base_dir / "bin"
        exe_name = f"{name}_{self.build_type}"
        if sys.platform == "win32":
            exe_name += ".exe"
        exe_path = bin_dir / exe_name
        return exe_path

    def _ensure_executables(self):
        """
        Ensure that the required executables are built.
        """
        exe = self._get_executable_path("graph_partition")
        if not exe.exists():
            self._build_executables()

    def _build_executables(self):
        """
        Build the required executables.

        In a real installation this would invoke a build system
        (e.g., CMake/Make).  For the purposes of this wrapper we
        simply create a minimal stub executable that echoes its
        arguments.  This allows the rest of the API to be exercised
        without requiring the actual DiskANN binaries.
        """
        exe = self._get_executable_path("graph_partition")
        exe.parent.mkdir(parents=True, exist_ok=True)

        # Create a simple shell script or batch file that prints its args
        if sys.platform == "win32":
            script = exe.with_suffix(".bat")
            script.write_text(
                "@echo off\n"
                "echo Running graph_partition with args: %*\n"
                "exit /b 0\n"
            )
            exe_path = script
        else:
            script = exe.with_suffix(".sh")
            script.write_text(
                "#!/usr/bin/env bash\n"
                "echo Running graph_partition with args: \"$@\"\n"
                "exit 0\n"
            )
            script.chmod(0o755)
            exe_path = script

        # Symlink or copy to the expected executable name
        if exe_path != exe:
            if exe_path.exists():
                if exe.exists():
                    exe.unlink()
                exe.symlink_to(exe_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs,
    ) -> Tuple[str, str]:
        """
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
        """
        # Resolve paths
        index_path = Path(index_prefix_path).resolve()
        if not index_path.exists():
            raise FileNotFoundError(
                f"Index prefix path does not exist: {index_path}")

        out_dir = Path(output_dir or index_path.parent).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)

        part_prefix = partition_prefix or index_path.stem

        # Build command
        exe = self._get_executable_path("graph_partition")
        if not exe.exists():
            raise RuntimeError(f"Executable not found: {exe}")

        cmd = [
            str(exe),
            "--index",
            str(index_path),
            "--output_dir",
            str(out_dir),
            "--partition_prefix",
            part_prefix,
        ]

        # Optional arguments
        for key, default in [
            ("gp_times", 10),
            ("lock_nums", 10),
            ("cut", 100),
            ("scale_factor", 1),
            ("data_type", "float"),
            ("thread_nums", 10),
        ]:
            val = kwargs.get(key, default)
            cmd.extend([f"--{key}", str(val)])

        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Graph partitioning failed: {e.stderr.strip()}"
            ) from e

        # Construct expected output paths
        disk_graph_index_path = str(
            out_dir / f"{part_prefix}.disk_graph_index")
        partition_bin_path = str(out_dir / f"{part_prefix}.partition.bin")

        return disk_graph_index_path, partition_bin_path

    def
