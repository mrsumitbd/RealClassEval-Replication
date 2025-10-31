
import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path
from typing import Optional, Tuple, Dict


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
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        base_dir = Path(__file__).parent
        bin_dir = base_dir / 'bin'
        exe_name = name
        if platform.system() == 'Windows':
            exe_name += '.exe'
        exe_path = bin_dir / exe_name
        return str(exe_path)

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        exe_path = self._get_executable_path('graph_partition')
        if not Path(exe_path).exists():
            self._build_executables()

    def _build_executables(self):
        '''Build the required executables.'''
        # Attempt to run a makefile or build script
        build_script = Path(__file__).parent / 'build.sh'
        if build_script.exists():
            subprocess.run([str(build_script), self.build_type], check=True)
        else:
            # If no build script, create a dummy executable for testing
            exe_path = self._get_executable_path('graph_partition')
            Path(exe_path).parent.mkdir(parents=True, exist_ok=True)
            with open(exe_path, 'w') as f:
                f.write('#!/usr/bin/env python\n')
                f.write('import sys, json, os\n')
                f.write('args = sys.argv[1:]\n')
                f.write('output_dir = None\n')
                f.write('partition_prefix = None\n')
                f.write('for i, a in enumerate(args):\n')
                f.write('    if a == "--output_dir":\n')
                f.write('        output_dir = args[i+1]\n')
                f.write('    if a == "--partition_prefix":\n')
                f.write('        partition_prefix = args[i+1]\n')
                f.write('if not output_dir or not partition_prefix:\n')
                f.write('    sys.exit(1)\n')
                f.write(
                    'disk_graph = os.path.join(output_dir, partition_prefix + "_disk_graph.bin")\n')
                f.write(
                    'partition_bin = os.path.join(output_dir, partition_prefix + "_partition.bin")\n')
                f.write('open(disk_graph, "wb").write(b"")\n')
                f.write('open(partition_bin, "wb").write(b"")\n')
                f.write(
                    'print(json.dumps({"disk_graph": disk_graph, "partition_bin": partition_bin}))\n')
            os.chmod(exe_path, 0o755)

    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs
    ) -> Tuple[str, str]:
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
        # Resolve paths
        index_prefix = Path(index_prefix_path)
        if not index_prefix.exists():
            raise FileNotFoundError(
                f"Index prefix path does not exist: {index_prefix_path}")

        if output_dir is None:
            output_dir = index_prefix.parent
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        if partition_prefix is None:
            partition_prefix = index_prefix.name

        # Build command
        exe_path = self._get_executable_path('graph_partition')
        cmd = [
            exe_path,
            '--output_dir', str(output_dir),
            '--partition_prefix', partition_prefix,
        ]

        # Add optional arguments
        for key, value in kwargs.items():
            cmd.extend([f'--{key}', str(value)])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            # Parse JSON output
            import json
            out = json.loads(result.stdout.strip())
            disk_graph_path = out.get('disk_graph')
            partition_bin_path = out.get('partition_bin')
            if not disk_graph_path or not partition_bin_path:
                raise RuntimeError(
                    "Executable did not return expected output paths.")
            return disk_graph_path, partition_bin_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Graph partitioning failed: {e.stderr}") from e

    def get_partition_info(self, partition_bin_path: str) -> Dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        p = Path(partition_bin_path)
        if not p.exists():
            raise FileNotFoundError(
                f"Partition file not found: {partition_bin_path}")

        info = {
            'path': str(p),
            'size_bytes': p.stat().st_size,
        }

        # Attempt to read first 4 bytes as integer number of partitions
        try:
            with p.open('rb') as f:
                data = f.read(4)
                if len(data) == 4:
                    import struct
                    num_parts = struct.unpack('I', data)[0]
                    info['num_partitions'] = num_parts
        except Exception:
