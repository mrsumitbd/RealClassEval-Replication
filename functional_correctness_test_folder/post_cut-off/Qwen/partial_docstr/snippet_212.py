
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess
import os


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
        try:
            version = subprocess.check_output(
                [path, '-version'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')[0].split(' ')[2]
            return version
        except Exception as e:
            self.logger.error(
                f"Failed to extract Vivado version from path {path}: {e}")
            raise VivadoIntegrationError(
                f"Failed to extract Vivado version from path {path}") from e

    def _is_running_in_container(self) -> bool:
        return os.path.exists('/.dockerenv') or os.path.isfile('/proc/self/cgroup') and any('docker' in line for line in open('/proc/self/cgroup'))

    def _run_vivado_on_host(self) -> None:
        if not self._is_running_in_container():
            self.logger.error(
                "Attempted to run Vivado on host, but not running in a container.")
            raise VivadoIntegrationError(
                "Not running in a container, cannot drop to host for Vivado execution.")

        try:
            subprocess.run([self.vivado_path, '-mode', 'batch',
                           '-source', str(self.output_dir / 'run.tcl')], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Vivado execution failed: {e}")
            raise VivadoIntegrationError("Vivado execution failed") from e

    def run(self) -> None:
        if self._is_running_in_container():
            self._run_vivado_on_host()
        else:
            try:
                subprocess.run([self.vivado_path, '-mode', 'batch',
                               '-source', str(self.output_dir / 'run.tcl')], check=True)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Vivado execution failed: {e}")
                raise VivadoIntegrationError("Vivado execution failed") from e

    def get_vivado_info(self) -> Dict[str, str]:
        version = self._extract_version_from_path(self.vivado_path)
        return {
            'version': version,
            'board': self.board,
            'output_dir': str(self.output_dir),
            'vivado_path': self.vivado_path,
            'device_config': str(self.device_config)
        }
