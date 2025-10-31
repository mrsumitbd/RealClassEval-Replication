
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess
import os


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger if logger else logging.getLogger(__name__)
        self.device_config = device_config if device_config else {}

    def _extract_version_from_path(self, path: str) -> str:
        parts = path.split('/')
        for part in parts:
            if part.startswith('Vivado_'):
                return part.split('_')[1]
        return "unknown"

    def _is_running_in_container(self) -> bool:
        return os.path.exists('/.dockerenv') or os.path.isfile('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        vivado_cmd = f"{self.vivado_path}/bin/vivado"
        cmd = [vivado_cmd, "-mode", "batch", "-source", "script.tcl"]
        try:
            subprocess.run(cmd, check=True, cwd=str(self.output_dir))
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to run Vivado: {e}")
            raise

    def run(self) -> None:
        if self._is_running_in_container():
            raise RuntimeError("Cannot run Vivado inside a container.")
        self._run_vivado_on_host()

    def get_vivado_info(self) -> Dict[str, str]:
        version = self._extract_version_from_path(self.vivado_path)
        return {
            "version": version,
            "path": self.vivado_path,
            "board": self.board
        }
