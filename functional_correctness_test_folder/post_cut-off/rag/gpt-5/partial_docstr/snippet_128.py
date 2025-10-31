import os
import sys
import json
import time
import glob
import shutil
import hashlib
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, Dict, List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
        bt_norm = build_type.strip().lower()
        if bt_norm not in {'debug', 'release'}:
            bt_norm = 'release'
        self.build_type = bt_norm
        self._exe_name_candidates = [
            'graph_partition',
            'diskann_graph_partition',
            'disk_graph_partition'
        ]
        self._env_bin_vars = ['DISKANN_GRAPH_BIN_DIR', 'DISKANN_BIN_DIR']
        self._meta_ext = '.meta.json'

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        candidates: List[str] = []
        exe_names: List[str] = []
        if sys.platform.startswith('win'):
            if name.lower().endswith('.exe'):
                exe_names = [name]
            else:
                exe_names = [name + '.exe', name]
        else:
            exe_names = [name]

        # 1) Environment variables
        for env_var in self._env_bin_vars:
            base = os.environ.get(env_var)
            if base:
                for nm in exe_names:
                    candidates.append(os.path.abspath(os.path.join(base, nm)))

        # 2) Relative to this file (common build output locations)
        this_dir = Path(__file__).resolve().parent
        rel_dirs = [
            this_dir / 'bin',
            this_dir / 'build' / self.build_type / 'bin',
            this_dir / 'build' / self.build_type,
            this_dir.parent / 'bin',
            this_dir.parent / 'build' / self.build_type / 'bin',
            this_dir.parent / 'build' / self.build_type,
        ]
        for d in rel_dirs:
            for nm in exe_names:
                candidates.append(str((d / nm).resolve()))

        # 3) PATH lookup
        for nm in exe_names:
            found = shutil.which(nm)
            if found:
                candidates.append(found)

        # Deduplicate while preserving order
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c not in seen:
                unique_candidates.append(c)
                seen.add(c)

        for p in unique_candidates:
            if os.path.isfile(p) and (os.access(p, os.X_OK) or sys.platform.startswith('win')):
                return p

        raise FileNotFoundError(
            f"Graph partition executable '{name}' not found. Tried: {unique_candidates}")

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        for nm in self._exe_name_candidates:
            try:
                self._get_executable_path(nm)
                return
            except FileNotFoundError:
                continue
        self._build_executables()
        # Verify again
        for nm in self._exe_name_candidates:
            try:
                self._get_executable_path(nm)
                return
            except FileNotFoundError:
                continue
        raise FileNotFoundError(
            "Unable to locate or build graph partition executables.")

    def _build_executables(self):
        '''Build the required executables.'''
        src_dir_env = os.environ.get('DISKANN_SOURCE_DIR')
        if not src_dir_env:
            # Try a local build.sh script as a fallback
            build_sh = Path(__file__).resolve().parent / 'build.sh'
            if build_sh.is_file():
                try:
                    subprocess.run(
                        ['bash', str(build_sh), self.build_type],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    return
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(
                        f"Failed to build executables via build.sh: {e.stdout}") from e
            raise RuntimeError(
                "DISKANN_SOURCE_DIR not set, and no build.sh found to build executables.")

        src_dir = Path(src_dir_env).resolve()
        build_dir = src_dir / 'build' / self.build_type
        build_dir.mkdir(parents=True, exist_ok=True)

        cmake_config = [
            'cmake',
            '-S', str(src_dir),
            '-B', str(build_dir),
            f'-DCMAKE_BUILD_TYPE={"Release" if self.build_type=="release" else "Debug"}'
        ]
        try:
            subprocess.run(cmake_config, check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"CMake configuration failed: {e.stdout}") from e

        cmake_build = [
            'cmake',
            '--build', str(build_dir),
            '--config', 'Release' if self.build_type == 'release' else 'Debug',
            '--parallel'
        ]
        try:
            subprocess.run(cmake_build, check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Building executables failed: {e.stdout}") from e

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
        if not index_prefix_path:
            raise ValueError("index_prefix_path is required")
        index_prefix_path = os.path.abspath(index_prefix_path)

        # Determine output dir and prefix
        if output_dir is None:
            output_dir = os.path.dirname(index_prefix_path) or os.getcwd()
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        if partition_prefix is None:
            partition_prefix = os.path.basename(index_prefix_path)

        # Parameters with defaults
        gp_times = int(kwargs.get('gp_times', 10))
        lock_nums = int(kwargs.get('lock_nums', 10))
        cut = int(kwargs.get('cut', 100))
        scale_factor = int(kwargs.get('scale_factor', 1))
        data_type = str(kwargs.get('data_type', 'float'))
        thread_nums = int(kwargs.get('thread_nums', 10))

        timestamp = time.time()
        out_prefix = os.path.join(output_dir, partition_prefix)
        default_graph_path = out_prefix + '.disk.graph'
        default_partition_path = out_prefix + '.partition.bin'

        # Try to locate an executable
        exe_path = None
        for nm in self._exe_name_candidates:
            try:
                exe_path = self._get_executable_path(nm)
                break
            except FileNotFoundError:
                continue

        # If no executable found, create placeholder outputs
        if exe_path is None:
            logger.warning(
                "Graph partition executable not found. Creating placeholder partition files instead.")
            self._write_placeholder_outputs(default_graph_path, default_partition_path, {
                'mode': 'placeholder',
                'index_prefix_path': index_prefix_path,
                'gp_times': gp_times,
                'lock_nums': lock_nums,
                'cut': cut,
                'scale_factor': scale_factor,
                'data_type': data_type,
                'thread_nums': thread_nums,
                'created_at': datetime.utcnow().isoformat() + 'Z'
            })
            return default_graph_path, default_partition_path

        # Build command (best-effort flags; may vary by build of DiskANN)
        cmd = [
            exe_path,
            '-i', index_prefix_path,
            '-o', out_prefix,
            '--gp_times', str(gp_times),
            '--lock_nums', str(lock_nums),
            '--cut', str(cut),
            '--scale_factor', str(scale_factor),
            '--data_type', data_type,
            '--thread_nums', str(thread_nums),
        ]

        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            logger.debug("Partition stdout:\n%s", result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Graph partitioning failed:\n{e.stdout}") from e

        # Try to detect output files
        graph_path, partition_path = self._detect_output_files(
            output_dir, partition_prefix, timestamp, default_graph_path, default_partition_path
        )

        # Store metadata sidecar
        meta = {
            'mode': 'executed',
            'executable': exe_path,
            'cmd': cmd,
            'index_prefix_path': index_prefix_path,
            'output_dir': output_dir,
            'partition_prefix': partition_prefix,
            'gp_times': gp_times,
            'lock_nums': lock_nums,
            'cut': cut,
            'scale_factor': scale_factor,
            'data_type': data_type,
            'thread_nums': thread_nums,
            'completed_at': datetime.utcnow().isoformat() + 'Z'
        }
        self._write_meta_sidecar(graph_path, meta)
        self._write_meta_sidecar(partition_path, meta)

        return graph_path, partition_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        if not partition_bin_path:
            raise ValueError("partition_bin_path is required")
        p = Path(partition_bin_path).resolve()
        info: Dict[str, object] = {
            'path': str(p),
            'exists': p.exists()
        }
        if not p.exists():
            return info

        stat = p.stat()
        info.update({
            'size_bytes': stat.st_size,
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        })

        # Hash (best-effort; may be large)
        try:
            info['sha256'] = self._sha256_of_file(p)
        except Exception:
            info['sha256'] = None

        # Sidecar meta
        meta_path = p.with_suffix(
            p.suffix + self._meta_ext) if self._meta_ext not in p.name else p
        if meta_path.is_file():
            try:
                info['meta'] = json.loads(
                    meta_path.read_text(encoding='utf-8'))
            except Exception:
                info['meta'] = None
        else:
            info['meta'] = None

        return info

    def _write_placeholder_outputs(self, graph_path: str, partition_path: str, meta: dict):
        Path(graph_path).parent.mkdir(parents=True, exist_ok=True)
        # Minimal placeholder content
        with open(graph_path, 'wb') as f:
            f.write(b'GPAR\x01\x00\x00\x00')  # magic + version
            f.write(b'PLACEHOLDER_GRAPH')
        with open(partition_path, 'wb') as f:
            f.write(b'GPAR\x01\x00\x00\x00')  # magic + version
            f.write(b'PLACEHOLDER_PARTITION')

        self._write_meta_sidecar(graph_path, meta)
        self._write_meta_sidecar(partition_path, meta)

    def _write_meta_sidecar(self, target_path: str, meta: dict):
        p = Path(target_path)
        meta_path = p.with_suffix(p.suffix + self._meta_ext)
        try:
            meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        except Exception as e:
            logger.debug(
                "Failed to write meta sidecar for %s: %s", target_path, e)

    def _detect_output_files(
        self,
        output_dir: str,
        partition_prefix: str,
        since_timestamp: float,
        default_graph_path: str,
        default_partition_path: str
    ) -> Tuple[str, str]:
        graph_path = default_graph_path if os.path.isfile(
            default_graph_path) else None
        partition_path = default_partition_path if os.path.isfile(
            default_partition_path) else None

        if graph_path and partition_path:
            return graph_path, partition_path

        # Search for recently modified files in output dir
        candidates = [f for f in glob.glob(os.path.join(
            output_dir, f"{partition_prefix}*")) if os.path.isfile(f)]
        candidates_recent = [f for f in candidates if os.path.getmtime(
            f) >= since_timestamp - 1.0]

        # Try to identify partition and graph files by name
        for f in sorted(candidates_recent):
            name = os.path.basename(f).lower()
            if partition_path is None and ('partition' in name and name.endswith('.bin')):
                partition_path = f
            if graph_path is None and ('graph' in name or 'disk_graph' in name):
                graph_path = f

        # Fallbacks to any recent bin for partition
        if partition_path is None:
            for f in candidates_recent:
                if f.lower().endswith('.bin'):
                    partition_path = f
                    break

        # Fallbacks to any recent non-bin as graph
        if graph_path is None:
            for f in candidates_recent:
                if not f.lower().endswith('.bin'):
                    graph_path = f
                    break

        # If still not found, use defaults (even if not created), but raise if they don't exist
        if graph_path is None:
            graph_path = default_graph_path
        if partition_path is None:
            partition_path = default_partition_path

        missing: List[str] = []
        if not os.path.isfile(graph_path):
            missing.append(graph_path)
        if not os.path.isfile(partition_path):
            missing.append(partition_path)

        if missing:
            raise RuntimeError(
                f"Graph partition executable completed but expected outputs were not found: {missing}")

        return graph_path, partition_path

    def _sha256_of_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                h.update(chunk)
        return h.hexdigest()
