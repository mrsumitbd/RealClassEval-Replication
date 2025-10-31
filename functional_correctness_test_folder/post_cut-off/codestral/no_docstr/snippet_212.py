
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):

        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

    def _extract_version_from_path(self, path: str) -> str:

        version_pattern = re.compile(r'Vivado/(\d+\.\d+)')
        match = version_pattern.search(path)
        if match:
            return match.group(1)
        return "unknown"

    def _is_running_in_container(self) -> bool:

        return os.path.exists('/.dockerenv')

    def _run_vivado_on_host(self) -> None:

        vivado_version = self._extract_version_from_path(self.vivado_path)
        vivado_command = f"{self.vivado_path}/bin/vivado -mode batch -source {self.output_dir}/vivado_script.tcl -notrace -nolog"
        self.logger.info(
            f"Running Vivado {vivado_version} on host: {vivado_command}")
        subprocess.run(vivado_command, shell=True, check=True)

    def run(self) -> None:

        if self._is_running_in_container():
            self.logger.info("Running Vivado in container")
            # Add container-specific logic here
        else:
            self._run_vivado_on_host()

    def get_vivado_info(self) -> Dict[str, str]:

        vivado_version = self._extract_version_from_path(self.vivado_path)
        return {
            "board": self.board,
            "vivado_version": vivado_version,
            "output_dir": str(self.output_dir),
            "vivado_path": self.vivado_path,
        }
