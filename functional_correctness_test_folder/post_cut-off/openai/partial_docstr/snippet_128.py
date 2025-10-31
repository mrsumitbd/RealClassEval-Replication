
import os
import subprocess
import sys
import json
import re
import struct
from pathlib import Path
from typing import Optional, Tuple, Dict


class GraphPartitioner:
    '''
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    '''

    def __init__(self, build_type: str = 'release'):
        """
        Parameters
        ----------
        build_type : str, optional
            Build type for the executables ('release' or 'debug'). Defaults to 'release'.
        """
        self.build_type = build_type.lower()
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        """
        Resolve the absolute path to an executable.

        Parameters
        ----------
        name : str
            Name of the executable (e.g., 'diskann_partition').

        Returns
        -------
        str
            Absolute path to the executable.

        Raises
        ------
        FileNotFoundError
            If the executable cannot be found.
        """
        base_dir = Path(__file__).resolve().parent
        bin_dir = base_dir / 'bin' / self.build_type
        exe_path = bin_dir / name
        if sys.platform == 'win32':
            exe_path = exe_path.with_suffix('.exe')
        if not exe_path.is_file():
            raise FileNotFoundError(
                f"Executable '{name}' not found at {exe_path}")
        return str(exe_path)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        try:
            self._get_executable_path('diskann_partition')
        except FileNotFoundError:
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        build_dir = Path(__file__).resolve().parent / 'build'
        if not build_dir.is_dir():
            raise RuntimeError(f"Build directory not found: {build_dir}")

        # Run make with the appropriate build type
        make_cmd = ['make', f'BUILD_TYPE={self.build_type}']
        result = subprocess.run(
            make_cmd,
            cwd=build_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to build executables:\n{result.stdout}\n{result.stderr}"
            )

        # Verify that the executables now exist
        try:
            self._get_executable_path('diskann_partition')
        except FileNotFoundError as e:
            raise RuntimeError(f"Executable still missing after build: {e}")

    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs
    ) -> Tuple[str, str]:
        '''
        Partition a disk-based index for improved performance.

        Parameters
        ----------
        index_prefix_path : str
            Path to the index prefix (e.g., "/path/to/index").
        output_dir : Optional[str], optional
            Output directory for results (defaults to parent of index_prefix_path).
        partition_prefix : Optional[str], optional
            Prefix for output files (defaults to basename of index_prefix_path).
        **kwargs : dict
            Additional parameters for graph partitioning:
                - gp_times : int, default 10
                - lock_nums : int, default 10
                - cut : int, default 100
                - scale_factor : float, default 1.0
                - data_type : str, default "float"
                - thread_nums : int, default 10

        Returns
        -------
        Tuple[str, str]
            Tuple of (disk_graph_index_path, partition_bin_path).

        Raises
        ------
        RuntimeError
            If the partitioning process fails.
        '''
        # Resolve paths
        index_prefix = Path(index_prefix_path).resolve()
        if not index_prefix.exists():
            raise FileNotFoundError(f"Index prefix not found: {index_prefix}")

        out_dir = Path(output_dir or index_prefix.parent).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)

        part_prefix = partition_prefix or index_prefix.name

        # Build command
        exe_path = self._get_executable_path('diskann_partition')
        cmd = [
            exe_path,
            '--index_prefix', str(index_prefix),
            '--output_dir', str(out_dir),
            '--partition_prefix', part_prefix,
        ]

        # Default parameters
        defaults = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1.0,
            'data_type': 'float',
            'thread_nums': 10,
        }
        params = {**defaults, **kwargs}

        # Append parameters
        for key, value in params.items():
            cmd.extend([f'--{key}', str(value)])

        # Execute
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Graph partitioning failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        # Parse output for paths
        disk_graph_index_path = None
        partition_bin_path = None

        # Expected output lines:
        # "disk_graph_index_path: <path>"
        # "partition_bin_path: <path>"
        for line in result.stdout.splitlines():
            if line.startswith('disk_graph_index_path:'):
                disk_graph_index_path = line.split(':', 1)[1].strip()
            elif line.startswith('partition_bin_path:'):
                partition_bin_path = line.split(':', 1)[1].strip()

        if not disk_graph_index_path or not partition_bin_path:
            # Try to infer from known naming convention
            disk_graph_index_path = str(
                out_dir / f"{part_prefix}_disk_graph_index.bin")
            partition_bin_path = str(out_dir / f"{part_prefix}_partition.bin")

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> Dict:
        '''
        Get information about a partition file.

        Parameters
        ----------
        partition_bin_path : str
            Path to the partition binary file.

        Returns
        -------
        dict
            Dictionary containing partition information.
        '''
        part_path = Path(partition_bin_path).resolve()
        if not part_path.is_file():
            raise FileNotFoundError(f"Partition file not found: {part_path}")

        # The binary format is assumed to start with two 32-bit little-endian integers:
        #   - number of partitions
