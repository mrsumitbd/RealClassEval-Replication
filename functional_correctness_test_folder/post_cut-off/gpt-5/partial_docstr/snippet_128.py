import os
import sys
import json
import shutil
import hashlib
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict, List


class GraphPartitioner:
    '''
    A Python interface for DiskANN's graph partition functionality.
    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    '''

    def __init__(self, build_type: str = 'release'):
        self.build_type = build_type.lower()
        if self.build_type not in ('release', 'debug', 'relwithdebinfo', 'minsizerel'):
            self.build_type = 'release'
        self._partition_exec_name_candidates = [
            'graph_partition',
            'graph-partition',
            'diskann_graph_partition',
            'diskann-graph-partition',
        ]
        self._info_exec_name_candidates = [
            'graph_partition_info',
            'graph-partition-info',
            'diskann_graph_partition_info',
            'diskann-graph-partition-info',
        ]
        self._partition_exec_path = None
        self._info_exec_path = None
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        exe_names: List[str] = []
        if os.name == 'nt':
            exe_names.append(f"{name}.exe")
        exe_names.append(name)

        here = Path(__file__).resolve().parent

        search_dirs = [
            here,
            here / 'bin',
            here / 'build' / self.build_type / 'bin',
            here / 'build' / self.build_type,
            here.parent / 'bin',
            here.parent / 'build' / self.build_type / 'bin',
            here.parent / 'build' / self.build_type,
        ]

        env_bin = os.environ.get('DISKANN_BIN_DIR')
        if env_bin:
            search_dirs.insert(0, Path(env_bin))

        for d in search_dirs:
            for exe in exe_names:
                candidate = d / exe
                if candidate.exists() and os.access(candidate, os.X_OK):
                    return str(candidate)

        # As a fallback, check PATH
        for exe in exe_names:
            on_path = shutil.which(exe)
            if on_path:
                return on_path

        # Default expected location (may not exist)
        return str((here / 'build' / self.build_type / 'bin' / exe_names[-1]).resolve())

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        self._partition_exec_path = None
        self._info_exec_path = None

        # Try to locate existing executables
        for name in self._partition_exec_name_candidates:
            p = self._get_executable_path(name)
            if os.path.exists(p) and os.access(p, os.X_OK):
                self._partition_exec_path = p
                break

        for name in self._info_exec_name_candidates:
            p = self._get_executable_path(name)
            if os.path.exists(p) and os.access(p, os.X_OK):
                self._info_exec_path = p
                break

        # If missing, try to build
        if not self._partition_exec_path or not self._info_exec_path:
            self._build_executables()
            # Re-resolve after build
            self._partition_exec_path = None
            self._info_exec_path = None
            for name in self._partition_exec_name_candidates:
                p = self._get_executable_path(name)
                if os.path.exists(p) and os.access(p, os.X_OK):
                    self._partition_exec_path = p
                    break
            for name in self._info_exec_name_candidates:
                p = self._get_executable_path(name)
                if os.path.exists(p) and os.access(p, os.X_OK):
                    self._info_exec_path = p
                    break

        if not self._partition_exec_path:
            # Provide a helpful error that indicates where we looked
            raise FileNotFoundError("Could not find 'graph partition' executable. "
                                    "Set DISKANN_BIN_DIR or ensure the binary is on PATH. "
                                    "Attempted to build but did not find the artifact.")
        # _info_exec_path is optional for get_partition_info; we will fall back to file stats

    def _build_executables(self):
        '''Build the required executables.'''
        root = Path(__file__).resolve().parent
        build_dir = root / 'build' / self.build_type
        build_dir.mkdir(parents=True, exist_ok=True)

        # Try CMake configure
        cmake_config_cmd = [
            'cmake',
            '-S', str(root),
            '-B', str(build_dir),
            f'-DCMAKE_BUILD_TYPE={self.build_type.capitalize()}'
        ]
        try:
            subprocess.run(cmake_config_cmd, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            # If cmake not available or configure failed, we silently skip; caller will get not found error
            return

        # Try to build expected targets if present; otherwise build all
        possible_targets = list(
            set(self._partition_exec_name_candidates + self._info_exec_name_candidates))
        build_cmd = ['cmake', '--build', str(build_dir), '--parallel']
        try:
            subprocess.run(build_cmd + ['--target'] + possible_targets,
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            # Try building without explicit targets (all)
            try:
                subprocess.run(build_cmd, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception:
                return

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
        exec_path = self._partition_exec_path
        if not exec_path or not os.path.exists(exec_path):
            raise RuntimeError("Partition executable not found.")

        index_prefix_path = os.path.abspath(index_prefix_path)
        if not os.path.exists(index_prefix_path) and not os.path.exists(index_prefix_path + ".index"):
            # Accept prefix without extension; presence is best-effort
            parent = os.path.dirname(index_prefix_path)
            if not parent or not os.path.exists(parent):
                raise FileNotFoundError(
                    f"Index prefix path not found: {index_prefix_path}")

        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path) or os.getcwd()
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        if partition_prefix is None:
            partition_prefix = os.path.basename(
                index_prefix_path.rstrip(os.sep)) or "partition"

        # Defaults
        params = {
            'gp_times': 10,
            'lock_nums': 10,
            'cut': 100,
            'scale_factor': 1,
            'data_type': 'float',
            'thread_nums': 10,
        }
        params.update({k: v for k, v in kwargs.items() if v is not None})

        # Build CLI args from params using --kebab-case
        def to_flag(k: str) -> str:
            return "--" + k.replace('_', '-')

        cmd = [exec_path,
               "--index-prefix", index_prefix_path,
               "--output-dir", output_dir,
               "--output-prefix", partition_prefix]

        for k, v in params.items():
            cmd.append(to_flag(k))
            cmd.append(str(v))

        env = os.environ.copy()
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Graph partitioning failed (exit {proc.returncode}). "
                               f"Command: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")

        # Try to infer output files
        disk_graph_index_path, partition_bin_path = self._infer_outputs(
            output_dir, partition_prefix)

        # Fallback: attempt to extract from stdout if inference failed
        if (not disk_graph_index_path or not os.path.exists(disk_graph_index_path)) or \
           (not partition_bin_path or not os.path.exists(partition_bin_path)):
            from_stdout = self._parse_output_paths_from_stdout(proc.stdout)
            disk_graph_index_path = disk_graph_index_path or from_stdout.get(
                'disk_graph_index')
            partition_bin_path = partition_bin_path or from_stdout.get(
                'partition_bin')

        # Validate existence
        if not partition_bin_path or not os.path.exists(partition_bin_path):
            raise RuntimeError("Partitioning did not produce a partition binary file. "
                               f"Tried to locate with prefix '{partition_prefix}' in '{output_dir}'.\n"
                               f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        if not disk_graph_index_path or not os.path.exists(disk_graph_index_path):
            # Not strictly required by all workflows, but expected by this interface
            # If missing, still return partition_bin_path and the best guess for index path
            disk_graph_index_path = disk_graph_index_path or os.path.join(
                output_dir, f"{partition_prefix}.disk_graph_index")

        return disk_graph_index_path, partition_bin_path

    def _infer_outputs(self, output_dir: str, partition_prefix: str) -> Tuple[Optional[str], Optional[str]]:
        dirp = Path(output_dir)
        candidates_graph = [
            f"{partition_prefix}.disk_graph",
            f"{partition_prefix}.disk_graph_index",
            f"{partition_prefix}.disk.index",
            f"{partition_prefix}.graph.index",
            f"{partition_prefix}.graph",
        ]
        candidates_part = [
            f"{partition_prefix}.partition.bin",
            f"{partition_prefix}.partitions.bin",
            f"{partition_prefix}.partition",
            f"{partition_prefix}.partition_info.bin",
            f"{partition_prefix}.partitions",
        ]
        graph_path = None
        part_path = None
        for name in candidates_graph:
            p = dirp / name
            if p.exists():
                graph_path = str(p)
                break
        if graph_path is None:
            # search loosely by prefix
            for p in dirp.glob(f"{partition_prefix}*"):
                if p.is_file() and any(s in p.name for s in ['disk_graph', 'graph', 'disk.index']):
                    graph_path = str(p)
                    break

        for name in candidates_part:
            p = dirp / name
            if p.exists():
                part_path = str(p)
                break
        if part_path is None:
            for p in dirp.glob(f"{partition_prefix}*"):
                if p.is_file() and 'part' in p.name:
                    part_path = str(p)
                    break

        return graph_path, part_path

    def _parse_output_paths_from_stdout(self, stdout: str) -> Dict[str, Optional[str]]:
        res: Dict[str, Optional[str]] = {
            'disk_graph_index': None, 'partition_bin': None}
        lines = stdout.splitlines()
        for ln in lines:
            lower = ln.lower()
            if 'disk' in lower and 'graph' in lower and ('write' in lower or 'output' in lower or 'saved' in lower):
                # Extract path-like artefact
                path = self._extract_path_like(ln)
                if path:
                    res['disk_graph_index'] = path
            if 'partition' in lower and ('bin' in lower or 'file' in lower) and ('write' in lower or 'output' in lower or 'saved' in lower):
                path = self._extract_path_like(ln)
                if path:
                    res['partition_bin'] = path
        return res

    def _extract_path_like(self, text: str) -> Optional[str]:
        # Naive path extraction: find substrings with separators and extensions
        tokens = text.replace('"', ' ').replace("'", " ").split()
        candidates = []
        for t in tokens:
            if (os.sep in t or ('\\' in t) or ('/' in t)) and ('.' in os.path.basename(t)):
                candidates.append(t.strip(",.;:"))
        # Prefer the last one
        return candidates[-1] if candidates else None

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        partition_bin_path = os.path.abspath(partition_bin_path)
        if not os.path.exists(partition_bin_path):
            raise FileNotFoundError(
                f"Partition file not found: {partition_bin_path}")

        # If an info executable is available, try it first
        if self._info_exec_path and os.path.exists(self._info_exec_path):
            cmd = [self._info_exec_path, "--partition-bin",
                   partition_bin_path, "--json"]
            proc = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.returncode == 0:
                try:
                    data = json.loads(proc.stdout)
                    return data
                except Exception:
                    pass  # Fall back to file stats

        # If a sidecar JSON exists, use it
        sidecar = self._find_sidecar_json(partition_bin_path)
        if sidecar and os.path.exists(sidecar):
            try:
                with open(sidecar, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        # Fallback: provide file stats and hash
        stat = os.stat(partition_bin_path)
        return {
            'path': partition_bin_path,
            'size_bytes': stat.st_size,
            'mtime': stat.st_mtime,
            'sha256': self._sha256_file(partition_bin_path),
        }

    def _find_sidecar_json(self, path: str) -> Optional[str]:
        p = Path(path)
        candidates = [
            p.with_suffix(p.suffix + '.json'),
            p.with_suffix('.json'),
            p.parent / (p.stem + '.json'),
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return None

    def _sha256_file(self, path: str, bufsize: int = 1024 * 1024) -> str:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            while True:
                b = f.read(bufsize)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()
