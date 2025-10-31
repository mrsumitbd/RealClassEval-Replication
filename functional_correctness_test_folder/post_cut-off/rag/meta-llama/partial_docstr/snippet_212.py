
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
        match = re.search(r'Vivado/([^/]+)/', path)
        if match:
            return match.group(1)
        raise ValueError(f"Could not extract Vivado version from path: {path}")

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        # Assuming the script to run Vivado is in the output_dir
        script_path = self.output_dir / 'run_vivado.sh'
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Using docker to run the script on the host
        # This is a simplified example and might need adjustments based on the actual containerization technology used
        subprocess.run(['docker', 'run', '--rm', '-v',
                       f'{self.output_dir}:/output', '-w', '/output', 'vivado_image', 'bash', str(script_path)])

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
            # Run Vivado directly
            vivado_bin = Path(self.vivado_path) / 'bin' / 'vivado'
            if not vivado_bin.exists():
                raise FileNotFoundError(
                    f"Vivado executable not found: {vivado_bin}")

            # Assuming there's a TCL script to run
            tcl_script = self.output_dir / 'project.tcl'
            if not tcl_script.exists():
                raise FileNotFoundError(f"TCL script not found: {tcl_script}")

            try:
                subprocess.run([str(vivado_bin), '-mode', 'batch',
                               '-source', str(tcl_script)], check=True)
            except subprocess.CalledProcessError as e:
                raise VivadoIntegrationError("Vivado execution failed") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        version = self._extract_version_from_path(self.vivado_path)
        return {
            'version': version,
            'path': self.vivado_path,
        }


class VivadoIntegrationError(Exception):
    pass
