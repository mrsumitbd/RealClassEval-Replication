import os
import sys
import json
import glob
import stat
import time
import shutil
import struct
import logging
import pathlib
import subprocess
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


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
        bt = (build_type or 'release').strip().lower()
        if bt not in ('release', 'debug'):
            raise ValueError('build_type must be "debug" or "release"')
        self.build_type = bt
        self._exe_cache: Dict[str, str] = {}
        self._exe_candidates = [
            'graph_partition',
            'diskann_graph_partition',
            'graph_partition_cli',
        ]
        self._bin_dirs = self._discover_bin_dirs()

    def _discover_bin_dirs(self):
        dirs = []
        envs = [
            os.getenv('DISKANN_BIN'),
            os.getenv('DISKANN_HOME'),
            os.getenv('DISKANN_ROOT'),
            os.getenv('DISKANN_DIR'),
        ]
        for e in envs:
            if not e:
                continue
            p = pathlib.Path(e)
            if p.is_file():
                dirs.append(str(p.parent))
                continue
            if (p / 'bin').is_dir():
                dirs.append(str(p / 'bin'))
            # CMake-style builds
            cm_build = 'Release' if self.build_type == 'release' else 'Debug'
            for cand in [
                p / 'build' / 'bin',
                p / 'build' / cm_build,
                p / 'build' / cm_build / 'bin',
                p / 'out' / cm_build,
                p / 'out' / cm_build / 'bin',
            ]:
                if cand.is_dir():
                    dirs.append(str(cand))
        # Relative to this file
        here = pathlib.Path(__file__).resolve().parent
        cm_build = 'Release' if self.build_type == 'release' else 'Debug'
        for cand in [
            here / 'bin',
            here / '..' / 'bin',
            here / '..' / 'build' / 'bin',
            here / '..' / 'build' / cm_build,
            here / '..' / 'build' / cm_build / 'bin',
        ]:
            if cand.exists():
                dirs.append(str(cand.resolve()))
        # Remove duplicates while preserving order
        seen = set()
        uniq = []
        for d in dirs:
            if d not in seen:
                seen.add(d)
                uniq.append(d)
        return uniq

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        if name in self._exe_cache and os.path.isfile(self._exe_cache[name]):
            return self._exe_cache[name]
        exe_names = [name]
        if sys.platform.startswith('win'):
            exe_names = [f'{name}.exe', name]
        # Allow env var override for a specific name
        override = os.getenv(f'{name.upper()}_PATH')
        if override and os.path.isfile(override):
            self._exe_cache[name] = override
            return override
        # Search known directories
        for d in self._bin_dirs:
            for en in exe_names:
                cand = os.path.join(d, en)
                if os.path.isfile(cand):
                    try:
                        st = os.stat(cand)
                        if sys.platform.startswith('win') or (st.st_mode & stat.S_IXUSR):
                            self._exe_cache[name] = cand
                            return cand
                        # If not executable on posix, still try to run via shell
                        self._exe_cache[name] = cand
                        return cand
                    except OSError:
                        continue
        # Search PATH
        for en in exe_names:
            found = shutil.which(en)
            if found:
                self._exe_cache[name] = found
                return found
        raise FileNotFoundError(
            f'Could not locate executable "{name}". Searched: PATH and {self._bin_dirs}')

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        for cand in self._exe_candidates:
            try:
                self._get_executable_path(cand)
                return
            except FileNotFoundError:
                continue
        self._build_executables()
        # Re-try after build
        for cand in self._exe_candidates:
            try:
                self._get_executable_path(cand)
                return
            except FileNotFoundError:
                continue
        raise FileNotFoundError('Unable to find or build any graph partition executable '
                                f'from candidates: {self._exe_candidates}')

    def _build_executables(self):
        '''Build the required executables.'''
        # Attempt to build using CMake if DISKANN_HOME or related env is present
        diskann_home = os.getenv('DISKANN_HOME') or os.getenv(
            'DISKANN_ROOT') or os.getenv('DISKANN_DIR')
        if not diskann_home:
            raise FileNotFoundError(
                'DISKANN_HOME/DISKANN_ROOT/DISKANN_DIR not set, cannot build executables.')
        src = pathlib.Path(diskann_home).resolve()
        if not src.exists():
            raise FileNotFoundError(
                f'DiskANN source directory does not exist: {src}')
        build_dir = src / 'build'
        build_dir.mkdir(parents=True, exist_ok=True)
        cfg = 'Release' if self.build_type == 'release' else 'Debug'
        try:
            subprocess.run(
                ['cmake', '-S', str(src), '-B', str(build_dir),
                 f'-DCMAKE_BUILD_TYPE={cfg}'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Try generic build first
            subprocess.run(
                ['cmake', '--build', str(build_dir), '--config', cfg],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Failed to build executables via CMake: {e.stderr or e.stdout}') from e
        # Refresh bin dirs post-build
        self._bin_dirs = self._discover_bin_dirs()

    def _pick_executable(self) -> str:
        last_err = None
        for name in self._exe_candidates:
            try:
                return self._get_executable_path(name)
            except FileNotFoundError as e:
                last_err = e
        if last_err:
            raise last_err
        raise FileNotFoundError('No executable candidates available')

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
        if not index_prefix_path or not isinstance(index_prefix_path, str):
            raise ValueError('index_prefix_path must be a non-empty string')
        ipath = pathlib.Path(index_prefix_path)
        if not ipath.exists():
            # Allow "prefix" not strictly existing if DiskANN uses multiple suffixes; warn only
            logger.warning(
                'Index prefix path does not exist: %s (continuing, relying on tool)', index_prefix_path)

        if output_dir is None:
            parent = ipath.parent if ipath.suffix or ipath.exists(
            ) else pathlib.Path(os.path.dirname(index_prefix_path) or '.')
            output_dir = str(parent.resolve())
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

        if partition_prefix is None:
            # Use basename of index prefix (strip extensions)
            base = os.path.basename(index_prefix_path.rstrip('/'))
            if not base:
                base = 'partition'
            partition_prefix = base

        gp_times = int(kwargs.pop('gp_times', 10))
        lock_nums = int(kwargs.pop('lock_nums', 10))
        cut = int(kwargs.pop('cut', 100))
        scale_factor = int(kwargs.pop('scale_factor', 1))
        data_type = str(kwargs.pop('data_type', 'float'))
        thread_nums = int(kwargs.pop('thread_nums', 10))

        self._ensure_executables()
        exe = self._pick_executable()

        cmd = [
            exe,
            '--index_prefix', index_prefix_path,
            '--output_dir', output_dir,
            '--partition_prefix', partition_prefix,
            '--gp_times', str(gp_times),
            '--lock_nums', str(lock_nums),
            '--cut', str(cut),
            '--scale_factor', str(scale_factor),
            '--data_type', data_type,
            '--thread_nums', str(thread_nums),
        ]
        # Pass any extra kwargs as --k v (snake_case -> kebab-case)
        for k, v in kwargs.items():
            if v is None:
                continue
            flag = f'--{k.replace("_", "-")}'
            cmd.extend([flag, str(v)])

        logger.debug('Running graph partition command: %s', ' '.join(cmd))
        try:
            proc = subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.stdout:
                logger.debug(proc.stdout)
            if proc.stderr:
                logger.debug(proc.stderr)
        except FileNotFoundError as e:
            raise RuntimeError(f'Partition executable not found: {e}') from e
        except subprocess.CalledProcessError as e:
            msg = e.stderr or e.stdout or str(e)
            raise RuntimeError(f'Graph partitioning failed: {msg}') from e

        # Expected outputs (best-effort guesses; also try to discover with glob)
        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}_disk_graph.index')
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}_partition.bin')

        if not os.path.exists(disk_graph_index_path):
            # Attempt alternative names
            patterns = [
                os.path.join(
                    output_dir, f'{partition_prefix}*disk*graph*.index'),
                os.path.join(
                    output_dir, f'{partition_prefix}*disk*graph*.bin'),
                os.path.join(output_dir, f'{partition_prefix}*graph*.index'),
                os.path.join(output_dir, f'{partition_prefix}*graph*.bin'),
            ]
            found = None
            for pat in patterns:
                matches = sorted(glob.glob(pat))
                if matches:
                    found = matches[0]
                    break
            if found:
                disk_graph_index_path = found

        if not os.path.exists(partition_bin_path):
            patterns = [
                os.path.join(output_dir, f'{partition_prefix}*partition*.bin'),
                os.path.join(output_dir, f'{partition_prefix}*partition*.idx'),
                os.path.join(output_dir, f'{partition_prefix}*partition*.dat'),
            ]
            found = None
            for pat in patterns:
                matches = sorted(glob.glob(pat))
                if matches:
                    found = matches[0]
                    break
            if found:
                partition_bin_path = found

        return (disk_graph_index_path, partition_bin_path)

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        p = pathlib.Path(partition_bin_path)
        info: Dict[str, object] = {
            'path': str(p),
            'exists': p.exists(),
        }
        if not p.exists():
            return info

        try:
            stat_res = p.stat()
            info.update({
                'size_bytes': stat_res.st_size,
                'modified_time': time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime(stat_res.st_mtime)),
            })
        except OSError:
            pass

        # If there is a sidecar JSON, prefer it
        sidecars = [p.with_suffix(p.suffix + '.json'), p.with_suffix('.json')]
        for sc in sidecars:
            if sc.exists():
                try:
                    with open(sc, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    if isinstance(meta, dict):
                        info.update(meta)
                    break
                except Exception:
                    pass

        # Try to infer number of partitions from header (best effort)
        try:
            with open(p, 'rb') as f:
                header = f.read(16)
                if len(header) >= 4:
                    n = struct.unpack('<I', header[:4])[0]
                    # Heuristic: reasonable upper bound
                    if 0 < n < 1_000_000_000:
                        info.setdefault('num_partitions', n)
        except Exception:
            pass

        return info
