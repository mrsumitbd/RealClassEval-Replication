import os
import shutil
import subprocess
import sys
import json
import hashlib
from datetime import datetime
from typing import Optional, Tuple


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
        build_type = (build_type or 'release').strip().lower()
        if build_type not in ('debug', 'release'):
            raise ValueError('build_type must be "debug" or "release"')
        self.build_type = build_type
        self._module_dir = os.path.dirname(os.path.abspath(__file__))
        self._bin_dirs = []
        env_bin = os.environ.get('DISKANN_BIN')
        if env_bin:
            self._bin_dirs.append(env_bin)
        self._bin_dirs.append(os.path.join(
            self._module_dir, 'bin', self.build_type))
        self._bin_dirs.append(os.path.join(self._module_dir, 'bin'))

    def _get_executable_path(self, name: str) -> str:
        '''Get the path to a graph partition executable.'''
        override = os.environ.get(f'DISKANN_{name.upper()}_EXE')
        if override and os.path.isfile(override) and os.access(override, os.X_OK):
            return os.path.abspath(override)

        candidates = []
        if name == 'graph_partition':
            base_names = ['graph_partition',
                          'diskann_graph_partition', 'graph-partition']
        elif name == 'partition_info':
            base_names = ['partition_info',
                          'diskann_partition_info', 'partition-info']
        else:
            base_names = [name]

        exts = ['']
        if sys.platform.startswith('win'):
            exts = ['.exe', '.bat', '.cmd', '']

        for bn in base_names:
            for ext in exts:
                candidates.append(bn + ext)

        for d in self._bin_dirs:
            for cand in candidates:
                p = os.path.join(d, cand)
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    return os.path.abspath(p)

        for cand in candidates:
            found = shutil.which(cand)
            if found:
                return os.path.abspath(found)

        raise FileNotFoundError(f'Executable for "{name}" not found. Searched candidates: {", ".join(candidates)}. '
                                f'Add it to PATH, set DISKANN_BIN, or set DISKANN_{name.upper()}_EXE.')

    def _ensure_executables(self):
        '''Ensure that the required executables are built.'''
        missing = []
        for name in ('graph_partition', 'partition_info'):
            try:
                self._get_executable_path(name)
            except FileNotFoundError:
                missing.append(name)
        if not missing:
            return
        try:
            self._build_executables()
        except Exception as e:
            raise RuntimeError(
                f'Unable to build required executables ({", ".join(missing)}): {e}') from e
        still_missing = []
        for name in missing:
            try:
                self._get_executable_path(name)
            except FileNotFoundError:
                still_missing.append(name)
        if still_missing:
            raise RuntimeError(
                f'Missing executables after build attempt: {", ".join(still_missing)}')

    def _build_executables(self):
        '''Build the required executables.'''
        src_candidates = []
        for env_var in ('DISKANN_SOURCE_DIR', 'DISKANN_SRC', 'DISKANN_HOME'):
            val = os.environ.get(env_var)
            if val:
                src_candidates.append(val)
        src_candidates.append(os.path.join(self._module_dir, 'cpp'))
        src_candidates.append(os.path.join(self._module_dir, 'src'))
        src_candidates.append(self._module_dir)

        cmake_src = None
        for c in src_candidates:
            cmakelists = os.path.join(c, 'CMakeLists.txt')
            if os.path.isfile(cmakelists):
                cmake_src = c
                break

        if not cmake_src:
            raise RuntimeError(
                'Could not locate DiskANN CMake project. Set DISKANN_SOURCE_DIR or install the CLI tools.')

        build_dir = os.path.join(cmake_src, f'build-{self.build_type}')
        os.makedirs(build_dir, exist_ok=True)

        cmake_build_type = 'Release' if self.build_type == 'release' else 'Debug'
        configure_cmd = ['cmake', '-S', cmake_src, '-B',
                         build_dir, f'-DCMAKE_BUILD_TYPE={cmake_build_type}']
        result = subprocess.run(
            configure_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f'CMake configure failed: {result.stderr or result.stdout}')

        build_cmd = ['cmake', '--build', build_dir,
                     '--config', cmake_build_type]
        result = subprocess.run(
            build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f'CMake build failed: {result.stderr or result.stdout}')

        # Try to locate built executables and place them in a bin dir
        out_bin = os.path.join(self._module_dir, 'bin', self.build_type)
        os.makedirs(out_bin, exist_ok=True)
        potential_names = [
            ('graph_partition', ['graph_partition',
             'diskann_graph_partition', 'graph-partition']),
            ('partition_info', ['partition_info',
             'diskann_partition_info', 'partition-info']),
        ]
        # Search build tree for executables
        for key, names in potential_names:
            found_any = False
            for root, _, files in os.walk(build_dir):
                for f in files:
                    for n in names:
                        if f == n or f.startswith(n):
                            src_path = os.path.join(root, f)
                            if os.access(src_path, os.X_OK):
                                shutil.copy2(
                                    src_path, os.path.join(out_bin, f))
                                found_any = True
                                break
                if found_any:
                    break

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str] = None, partition_prefix: Optional[str] = None, **kwargs) -> Tuple[str, str]:
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

        if output_dir is None or not str(output_dir).strip():
            output_dir = os.path.dirname(
                os.path.abspath(index_prefix_path)) or os.getcwd()
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        if partition_prefix is None or not str(partition_prefix).strip():
            partition_prefix = os.path.basename(
                index_prefix_path.rstrip(os.sep))

        gp_times = int(kwargs.get('gp_times', 10))
        lock_nums = int(kwargs.get('lock_nums', 10))
        cut = int(kwargs.get('cut', 100))
        scale_factor = float(kwargs.get('scale_factor', 1))
        data_type = str(kwargs.get('data_type', 'float'))
        thread_nums = int(kwargs.get('thread_nums', 10))

        self._ensure_executables()
        exe = self._get_executable_path('graph_partition')

        disk_graph_index_path = os.path.join(
            output_dir, f'{partition_prefix}.disk_graph.index')
        partition_bin_path = os.path.join(
            output_dir, f'{partition_prefix}.partition.bin')

        cmd = [
            exe,
            '-i', index_prefix_path,
            '-o', output_dir,
            '-p', partition_prefix,
            '-g', str(gp_times),
            '-l', str(lock_nums),
            '-c', str(cut),
            '-s', str(scale_factor),
            '-d', data_type,
            '-t', str(thread_nums),
        ]

        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            msg = result.stderr.strip() or result.stdout.strip() or 'Unknown error'
            raise RuntimeError(f'graph_partition failed: {msg}')

        if not os.path.exists(partition_bin_path) and not os.path.exists(disk_graph_index_path):
            # Try alternative common names if tool produced differently named outputs
            alt_partition = os.path.join(
                output_dir, f'{partition_prefix}.partition')
            alt_disk = os.path.join(
                output_dir, f'{partition_prefix}.disk_graph')
            if os.path.exists(alt_partition):
                partition_bin_path = alt_partition
            if os.path.exists(alt_disk):
                disk_graph_index_path = alt_disk

        # Final existence checks (do not enforce both; some workflows may only emit one)
        if not (os.path.exists(partition_bin_path) or os.path.exists(disk_graph_index_path)):
            raise RuntimeError(
                'Partitioning did not produce expected output files.')

        return disk_graph_index_path, partition_bin_path

    def get_partition_info(self, partition_bin_path: str) -> dict:
        '''
        Get information about a partition file.
        Args:
            partition_bin_path: Path to the partition binary file
        Returns:
            Dictionary containing partition information
        '''
        if not partition_bin_path or not os.path.isfile(partition_bin_path):
            raise FileNotFoundError(
                f'Partition file not found: {partition_bin_path}')

        info = {
            'path': os.path.abspath(partition_bin_path),
            'size_bytes': os.path.getsize(partition_bin_path),
            'modified_time': datetime.fromtimestamp(os.path.getmtime(partition_bin_path)).isoformat(),
            'sha256': self._sha256(partition_bin_path),
        }

        try:
            exe = self._get_executable_path('partition_info')
        except FileNotFoundError:
            return info

        cmd = [exe, '-i', partition_bin_path]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return info

        output = (result.stdout or '').strip()
        if not output:
            return info

        try:
            parsed = json.loads(output)
            if isinstance(parsed, dict):
                info.update(parsed)
                return info
        except json.JSONDecodeError:
            pass

        # Fallback parse key:value lines
        for line in output.splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                info[k.strip()] = v.strip()

        return info

    @staticmethod
    def _sha256(path: str) -> str:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                h.update(chunk)
        return h.hexdigest()
