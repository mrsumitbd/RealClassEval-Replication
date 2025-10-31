
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import re
import os


class VivadoIntegrationError(Exception):
    pass


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
        match = re.search(r'Vivado/(\d+\.\d+\.\d+)', path)
        if match:
            return match.group(1)
        raise VivadoIntegrationError(
            "Could not extract Vivado version from path")

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.isfile('/proc/self/cgroup') and any('docker' in line for line in open('/proc/self/cgroup'))

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        raise NotImplementedError(
            "Running Vivado on the host from a container is not yet implemented")

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
            vivado_executable = Path(self.vivado_path) / 'bin' / 'vivado'
            if not vivado_executable.exists():
                raise VivadoIntegrationError(
                    f"Vivado executable not found at {vivado_executable}")
            # Assuming a tcl script is generated and named 'run.tcl' in the output directory
            tcl_script = self.output_dir / 'run.tcl'
            if not tcl_script.exists():
                raise VivadoIntegrationError(
                    f"TCL script not found at {tcl_script}")
            command = f"{vivado_executable} -mode batch -source {tcl_script}"
            self.logger.info(f"Running Vivado with command: {command}")
            # Execute the command here, for example using subprocess
            # subprocess.run(command, shell=True, check=True)

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        version = self._extract_version_from_path(self.vivado_path)
        return {
            'version': version,
            'installation_path': self.vivado_path,
            'board': self.board,
            'output_directory': str(self.output_dir)
        }
