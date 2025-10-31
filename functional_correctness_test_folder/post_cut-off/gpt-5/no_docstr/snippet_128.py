import os
import sys
import json
import time
import hashlib
from typing import Optional, Tuple, Dict, Any


class GraphPartitioner:
    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type
        self._root = os.path.abspath(os.path.dirname(__file__))
        self._build_dir = os.path.join(self._root, 'build', build_type)
        self._exe_suffix = '.exe' if sys.platform.startswith('win') else ''
        self._executables = {
            'partitioner': self._get_executable_path('graph_partitioner'),
            'partition_info': self._get_executable_path('partition_info'),
        }

    def _get_executable_path(self, name: str) -> str:
        candidate = os.path.join(self._build_dir, name + self._exe_suffix)
        return candidate

    def _ensure_executables(self):
        # Placeholder to maintain interface compatibility
        # In this pure-python implementation, there are no external executables required.
        return

    def _build_executables(self):
        # Placeholder for build logic if external executables are needed in a different environment.
        # Not used in this implementation.
        return

    def partition_graph(
        self,
        index_prefix_path: str,
        output_dir: Optional[str] = None,
        partition_prefix: Optional[str] = None,
        **kwargs
    ) -> Tuple[str, str]:
        if not os.path.isfile(index_prefix_path):
            raise FileNotFoundError(
                f"Input file not found: {index_prefix_path}")

        num_partitions = int(kwargs.get('num_partitions', 2))
        if num_partitions <= 0:
            raise ValueError("num_partitions must be a positive integer")

        seed = kwargs.get('seed')
        if seed is None:
            seed_bytes = b''
        elif isinstance(seed, (bytes, bytearray)):
            seed_bytes = bytes(seed)
        else:
            seed_bytes = str(seed).encode('utf-8')

        if output_dir is None:
            output_dir = os.path.dirname(
                os.path.abspath(index_prefix_path)) or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        if partition_prefix is None:
            base = os.path.splitext(os.path.basename(index_prefix_path))[0]
            partition_prefix = f"{base}"

        partition_bin_path = os.path.join(
            output_dir, f"{partition_prefix}.partitions.tsv")
        partition_info_path = os.path.join(
            output_dir, f"{partition_prefix}.info.json")

        counts = [0] * num_partitions
        total = 0

        with open(index_prefix_path, 'r', encoding='utf-8') as fin, \
                open(partition_bin_path, 'w', encoding='utf-8') as fout:
            for line in fin:
                s = line.strip()
                if not s:
                    continue
                # Stable partition by hashing
                try:
                    # Try numeric path for light normalization, but treat as string ultimately
                    val_for_hash = str(int(s))
                except ValueError:
                    val_for_hash = s
                h = hashlib.blake2b(val_for_hash.encode(
                    'utf-8'), digest_size=8, person=seed_bytes).digest()
                pid = int.from_bytes(h, byteorder='little') % num_partitions
                counts[pid] += 1
                total += 1
                fout.write(f"{pid}\t{s}\n")

        info: Dict[str, Any] = {
            "input_file": os.path.abspath(index_prefix_path),
            "output_file": os.path.abspath(partition_bin_path),
            "num_partitions": num_partitions,
            "sizes": counts,
            "total_items": total,
            "seed": seed,
            "format": "tsv(pid, item)",
            "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "tool": "GraphPartitioner-python",
            "build_type": self.build_type,
        }

        with open(partition_info_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, sort_keys=True)

        return partition_bin_path, partition_info_path

    def get_partition_info(self, partition_bin_path: str) -> Dict[str, Any]:
        if not os.path.isfile(partition_bin_path):
            raise FileNotFoundError(
                f"Partition file not found: {partition_bin_path}")

        sidecar = os.path.splitext(partition_bin_path)[0] + ".info.json"
        if os.path.isfile(sidecar):
            with open(sidecar, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Reconstruct minimal info if sidecar is missing
        counts: Dict[int, int] = {}
        total = 0
        with open(partition_bin_path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                parts = s.split('\t')
                if not parts:
                    continue
                try:
                    pid = int(parts[0])
                except ValueError:
                    continue
                counts[pid] = counts.get(pid, 0) + 1
                total += 1

        if counts:
            max_pid = max(counts.keys())
            sizes = [counts.get(i, 0) for i in range(max_pid + 1)]
            num_partitions = len(sizes)
        else:
            sizes = []
            num_partitions = 0

        info = {
            "output_file": os.path.abspath(partition_bin_path),
            "num_partitions": num_partitions,
            "sizes": sizes,
            "total_items": total,
            "format": "tsv(pid, item)",
            "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "tool": "GraphPartitioner-python",
            "reconstructed": True,
        }
        return info
