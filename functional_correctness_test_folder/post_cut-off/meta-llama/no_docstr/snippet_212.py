
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger if logger else logging.getLogger(__name__)
        self.device_config = device_config if device_config else {}
        self.vivado_version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        import re
        match = re.search(r'Vivado/(\d+\.\d+)', path)
        return match.group(1) if match else 'unknown'

    def _is_running_in_container(self) -> bool:
        try:
            with open('/proc/self/cgroup', 'r') as f:
                return 'docker' in f.read() or 'kubepod' in f.read()
        except FileNotFoundError:
            return False

    def _run_vivado_on_host(self) -> None:
        vivado_cmd = f'{self.vivado_path}/bin/vivado -mode batch -source run_vivado.tcl'
        try:
            subprocess.run(vivado_cmd, shell=True,
                           check=True, cwd=self.output_dir)
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to run Vivado: {e}')

    def run(self) -> None:
        if self._is_running_in_container():
            self.logger.warning(
                'Running Vivado inside a container is not recommended.')
        self._run_vivado_on_host()

    def get_vivado_info(self) -> Dict[str, str]:
        return {
            'version': self.vivado_version,
            'path': self.vivado_path,
            'board': self.board,
        }
