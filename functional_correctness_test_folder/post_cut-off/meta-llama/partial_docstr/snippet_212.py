
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class VivadoIntegrationError(Exception):
    pass


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

    def _extract_version_from_path(self, path: str) -> str:
        import re
        match = re.search(r'Vivado/(\d+\.\d+)', path)
        return match.group(1) if match else 'unknown'

    def _is_running_in_container(self) -> bool:
        return Path('/.dockerenv').exists() or Path('/run/.containerenv').exists()

    def _run_vivado_on_host(self) -> None:
        # Assuming the script to run Vivado is generated and available at output_dir
        script_path = self.output_dir / 'run_vivado.sh'
        if not script_path.exists():
            raise VivadoIntegrationError("Vivado script not found")

        try:
            subprocess.run(['sh', str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            raise VivadoIntegrationError("Failed to run Vivado") from e

    def run(self) -> None:
        if self._is_running_in_container():
            self._run_vivado_on_host()
        else:
            try:
                vivado_cmd = f'{self.vivado_path} -mode batch -source {self.output_dir}/vivado_script.tcl'
                subprocess.run(vivado_cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise VivadoIntegrationError("Failed to run Vivado") from e

    def get_vivado_info(self) -> Dict[str, str]:
        vivado_version = self._extract_version_from_path(self.vivado_path)
        return {
            'vivado_version': vivado_version,
            'vivado_path': self.vivado_path,
            'is_container': str(self._is_running_in_container())
        }
