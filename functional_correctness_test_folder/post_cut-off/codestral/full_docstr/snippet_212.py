
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

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        version_pattern = re.compile(r'Vivado/(\d+\.\d+)')
        match = version_pattern.search(path)
        if match:
            return match.group(1)
        raise ValueError("Could not extract Vivado version from path")

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv')

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        if not self._is_running_in_container():
            return

        host_output_dir = self.output_dir.parent / \
            f"{self.output_dir.name}_host"
        host_output_dir.mkdir(exist_ok=True)

        vivado_script = self.output_dir / "vivado_script.tcl"
        host_vivado_script = host_output_dir / "vivado_script.tcl"

        with open(vivado_script, 'r') as f:
            script_content = f.read()

        with open(host_vivado_script, 'w') as f:
            f.write(script_content)

        subprocess.run(["docker", "run", "--rm", "-v", f"{host_output_dir}:/workspace",
                       "vivado", "vivado", "-mode", "batch", "-source", "/workspace/vivado_script.tcl"])

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self._run_vivado_on_host()
        else:
            vivado_script = self.output_dir / "vivado_script.tcl"
            subprocess.run([f"{self.vivado_path}/bin/vivado",
                           "-mode", "batch", "-source", str(vivado_script)])

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        version = self._extract_version_from_path(self.vivado_path)
        return {
            "version": version,
            "path": self.vivado_path,
            "board": self.board,
            "output_dir": str(self.output_dir)
        }
