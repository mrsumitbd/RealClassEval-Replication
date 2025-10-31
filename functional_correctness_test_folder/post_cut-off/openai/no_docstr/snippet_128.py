
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict

try:
    import networkx as nx
except ImportError:
    nx = None


class GraphPartitioner:
    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self.base_dir = Path(__file__).parent
        self.bin_dir = self.base_dir / 'bin' / self.build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> Path:
        return self.bin_dir / name

    def _ensure_executables(self):
        if not self.bin_dir.exists():
            self.bin_dir.mkdir(parents=True, exist_ok=True)
        # Check for required executables; if missing, build them
        required = ['graph_partition', 'graph_partition_info']
        missing = [
            name for name in required if not self._get_executable_path(name).exists()]
        if missing:
            self._build_executables()

    def _build_executables(self):
        # Dummy implementation: create simple shell scripts that echo arguments
        for name in ['graph_partition', 'graph_partition_info']:
            exe_path = self._get_executable_path(name)
            if sys.platform == 'win32':
                script = f"@echo off\npython -c \"import sys; print(' '.join(sys.argv[1:]))\""
                exe_path.write_text(script)
                exe_path.chmod(0o755)
            else:
                script = f"#!/usr/bin/env bash\npython -c \"import sys; print(' '.join(sys.argv[1:]))\""
                exe_path.write_text(script)
                exe_path.chmod(0o755)

    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs
    ) -> Tuple[str, str]:
        """
        Partition a graph file into two partitions using a simple random assignment.
        Returns a tuple of paths to the two partition files.
        """
        if nx is None:
            raise RuntimeError("networkx is required for graph partitioning")

        graph_path = Path(index_prefix_path)
        if not graph_path.exists():
            raise FileNotFoundError(f"Graph file not found: {graph_path}")

        G = nx.read_adjlist(graph_path, nodetype=str)

        num_partitions = kwargs.get('num_partitions', 2)
        if num_partitions < 1:
            raise ValueError("num_partitions must be at least 1")

        nodes = list(G.nodes())
        random.shuffle(nodes)
        partitions = [[] for _ in range(num_partitions)]
        for i, node in enumerate(nodes):
            partitions[i % num_partitions].append(node)

        out_dir = Path(output_dir) if output_dir else graph_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        prefix = partition_prefix or graph_path.stem
        partition_paths = []
        for idx, part_nodes in enumerate(partitions):
            part_file = out_dir / f"{prefix}_part{idx}.txt"
            part_file.write_text("\n".join(part_nodes))
            partition_paths.append(str(part_file))

        return tuple(partition_paths)

    def get_partition_info(self, partition_bin_path: str) -> Dict:
        """
        Reads a partition file and returns metadata such as number of nodes.
        """
        part_path = Path(partition_bin_path)
        if not part_path.exists():
            raise FileNotFoundError(f"Partition file not found: {part_path}")

        nodes = part_path.read_text().splitlines()
        return {
            'num_nodes': len(nodes),
            'nodes': nodes,
        }
