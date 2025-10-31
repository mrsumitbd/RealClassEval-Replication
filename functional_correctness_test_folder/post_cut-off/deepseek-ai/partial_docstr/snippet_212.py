
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import os


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

    def _extract_version_from_path(self, path: str) -> str:
        parts = path.split('/')
        for part in parts:
            if part.startswith('Vivado_'):
                return part.split('_')[1]
        return "unknown"

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{self.output_dir}:/workspace",
            "vivado-host",
            "/bin/bash",
            "-c",
            f"source {self.vivado_path}/settings64.sh && vivado -mode batch -source /workspace/script.tcl"
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run Vivado on host: {e}")

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            RuntimeError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self._run_vivado_on_host()
        else:
            cmd = [
                f"{self.vivado_path}/vivado",
                "-mode",
                "batch",
                "-source",
                f"{self.output_dir}/script.tcl"
            ]
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to run Vivado: {e}")

    def get_vivado_info(self) -> Dict[str, str]:
        version = self._extract_version_from_path(self.vivado_path)
        return {
            "version": version,
            "path": self.vivado_path,
            "board": self.board
        }
