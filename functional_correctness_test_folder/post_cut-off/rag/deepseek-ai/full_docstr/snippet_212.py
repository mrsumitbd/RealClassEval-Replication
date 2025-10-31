
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


class VivadoRunner:
    '''
    Handles everything Vivado SIMPLY
    Attributes:
        board: current target device
        output_dir: dir for generated vivado project
        vivado_path: root path to xilinx vivado installation (all paths derived from here)
        logger: attach a logger
    '''

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        '''Initialize VivadoRunner with simplified configuration.
        Args:
            board: Target board name (e.g., "pcileech_35t325_x1")
            output_dir: Directory for generated Vivado project
            vivado_path: Root path to Xilinx Vivado installation
            logger: Optional logger instance
            device_config: Optional device configuration dictionary
        '''
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}
        self.version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        match = re.search(r'Vivado[/\\](\d{4}\.\d+)', path)
        if not match:
            raise ValueError(
                f"Could not extract Vivado version from path: {path}")
        return match.group(1)

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.isfile('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        if not self._is_running_in_container():
            raise RuntimeError(
                "Not running in a container - cannot drop to host")

        cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.output_dir}:/workspace",
            "-v", f"{self.vivado_path}:/opt/Xilinx",
            "xilinx/vivado", "vivado",
            "-mode", "batch",
            "-source", f"/workspace/{self.board}_vivado.tcl"
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Vivado execution failed: {e}") from e

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self.logger.info(
                "Running in container - delegating to host system")
            self._run_vivado_on_host()
        else:
            self.logger.info("Running Vivado directly on host system")
            vivado_exec = str(Path(self.vivado_path) / "bin" / "vivado")
            cmd = [
                vivado_exec,
                "-mode", "batch",
                "-source", str(self.output_dir / f"{self.board}_vivado.tcl")
            ]
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Vivado execution failed: {e}") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        return {
            "version": self.version,
            "path": self.vivado_path,
            "board": self.board,
            "output_dir": str(self.output_dir),
            "in_container": str(self._is_running_in_container())
        }
