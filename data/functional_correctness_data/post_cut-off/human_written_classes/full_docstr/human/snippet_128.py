import shutil
from typing import Optional
import tempfile
import subprocess
from pathlib import Path
import os

class GraphPartitioner:
    """
    A Python interface for DiskANN's graph partition functionality.

    This class provides methods to partition disk-based indices for improved
    search performance and memory efficiency.
    """

    def __init__(self, build_type: str='release'):
        """
        Initialize the GraphPartitioner.

        Args:
            build_type: Build type for the executables ("debug" or "release")
        """
        self.build_type = build_type
        self._ensure_executables()

    def _get_executable_path(self, name: str) -> str:
        """Get the path to a graph partition executable."""
        module_dir = Path(__file__).parent
        graph_partition_dir = module_dir.parent / 'third_party' / 'DiskANN' / 'graph_partition'
        executable_path = graph_partition_dir / 'build' / self.build_type / 'graph_partition' / name
        if not executable_path.exists():
            raise FileNotFoundError(f'Executable {name} not found at {executable_path}')
        return str(executable_path)

    def _ensure_executables(self):
        """Ensure that the required executables are built."""
        try:
            self._get_executable_path('partitioner')
            self._get_executable_path('index_relayout')
        except FileNotFoundError:
            print('Executables not found, attempting to build them...')
            self._build_executables()

    def _build_executables(self):
        """Build the required executables."""
        graph_partition_dir = Path(__file__).parent.parent / 'third_party' / 'DiskANN' / 'graph_partition'
        original_dir = os.getcwd()
        try:
            os.chdir(graph_partition_dir)
            if (graph_partition_dir / 'build').exists():
                shutil.rmtree(graph_partition_dir / 'build')
            cmd = ['./build.sh', self.build_type, 'split_graph', '/tmp/dummy']
            subprocess.run(cmd, capture_output=True, text=True, cwd=graph_partition_dir)
            partitioner_path = self._get_executable_path('partitioner')
            relayout_path = self._get_executable_path('index_relayout')
            print(f'✅ Built partitioner: {partitioner_path}')
            print(f'✅ Built index_relayout: {relayout_path}')
        except Exception as e:
            raise RuntimeError(f'Failed to build executables: {e}')
        finally:
            os.chdir(original_dir)

    def partition_graph(self, index_prefix_path: str, output_dir: Optional[str]=None, partition_prefix: Optional[str]=None, **kwargs) -> tuple[str, str]:
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
        params = {'gp_times': 10, 'lock_nums': 10, 'cut': 100, 'scale_factor': 1, 'data_type': 'float', 'thread_nums': 10, **kwargs}
        if output_dir is None:
            output_dir = str(Path(index_prefix_path).parent)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        if partition_prefix is None:
            partition_prefix = Path(index_prefix_path).name
        partitioner_path = self._get_executable_path('partitioner')
        relayout_path = self._get_executable_path('index_relayout')
        with tempfile.TemporaryDirectory() as temp_dir:
            graph_partition_dir = Path(__file__).parent.parent / 'third_party' / 'DiskANN' / 'graph_partition'
            original_dir = os.getcwd()
            try:
                os.chdir(graph_partition_dir)
                temp_data_dir = Path(temp_dir) / 'data'
                temp_data_dir.mkdir(parents=True, exist_ok=True)
                graph_path = temp_data_dir / 'starling' / '_M_R_L_B' / 'GRAPH'
                graph_gp_path = graph_path / f"GP_TIMES_{params['gp_times']}_LOCK_{params['lock_nums']}_GP_USE_FREQ0_CUT{params['cut']}_SCALE{params['scale_factor']}"
                graph_gp_path.mkdir(parents=True, exist_ok=True)
                old_index_file = f'{index_prefix_path}_disk_beam_search.index'
                if not os.path.exists(old_index_file):
                    old_index_file = f'{index_prefix_path}_disk.index'
                if not os.path.exists(old_index_file):
                    raise RuntimeError(f'Index file not found: {old_index_file}')
                gp_file_path = graph_gp_path / '_part.bin'
                partitioner_cmd = [partitioner_path, '--index_file', old_index_file, '--data_type', params['data_type'], '--gp_file', str(gp_file_path), '-T', str(params['thread_nums']), '--ldg_times', str(params['gp_times']), '--scale', str(params['scale_factor']), '--mode', '1']
                print(f"Running partitioner: {' '.join(partitioner_cmd)}")
                result = subprocess.run(partitioner_cmd, capture_output=True, text=True, cwd=graph_partition_dir)
                if result.returncode != 0:
                    raise RuntimeError(f'Partitioner failed with return code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}')
                part_tmp_index = graph_gp_path / '_part_tmp.index'
                relayout_cmd = [relayout_path, old_index_file, str(gp_file_path), params['data_type'], '1']
                print(f"Running relayout: {' '.join(relayout_cmd)}")
                result = subprocess.run(relayout_cmd, capture_output=True, text=True, cwd=graph_partition_dir)
                if result.returncode != 0:
                    raise RuntimeError(f'Relayout failed with return code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}')
                disk_graph_path = Path(output_dir) / f'{partition_prefix}_disk_graph.index'
                partition_bin_path = Path(output_dir) / f'{partition_prefix}_partition.bin'
                shutil.copy2(part_tmp_index, disk_graph_path)
                shutil.copy2(gp_file_path, partition_bin_path)
                print(f'Results copied to: {output_dir}')
                return (str(disk_graph_path), str(partition_bin_path))
            finally:
                os.chdir(original_dir)

    def get_partition_info(self, partition_bin_path: str) -> dict:
        """
        Get information about a partition file.

        Args:
            partition_bin_path: Path to the partition binary file

        Returns:
            Dictionary containing partition information
        """
        if not os.path.exists(partition_bin_path):
            raise FileNotFoundError(f'Partition file not found: {partition_bin_path}')
        stat = os.stat(partition_bin_path)
        return {'file_size': stat.st_size, 'file_path': partition_bin_path, 'modified_time': stat.st_mtime}