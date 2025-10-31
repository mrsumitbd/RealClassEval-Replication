
import logging
import os
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
        self.vivado_version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Assuming the path is something like /opt/Xilinx/Vivado/2021.2/bin
        version = os.path.basename(os.path.dirname(os.path.dirname(path)))
        return version

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        # Check for the presence of /.dockerenv or /proc/1/cgroup
        return os.path.exists('/.dockerenv') or any('docker' in line for line in open('/proc/1/cgroup'))

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        # This is a placeholder for the actual logic to run Vivado on the host
        # For example, you might use a command like `docker exec` or `ssh` to the host
        self.logger.info("Running Vivado on the host system.")
        # Example command: subprocess.run(['ssh', 'user@host', f'{self.vivado_path}/bin/vivado', '-mode', 'batch', '-source', 'script.tcl'])
        raise NotImplementedError(
            "Running Vivado on the host is not yet implemented.")

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
            self.logger.info("Running Vivado in batch mode.")
            try:
                subprocess.run([f'{self.vivado_path}/bin/vivado', '-mode', 'batch',
                               '-source', 'script.tcl'], check=True, cwd=self.output_dir)
            except subprocess.CalledProcessError as e:
                self.logger.error("Vivado integration failed: %s", e)
                raise VivadoIntegrationError(
                    "Vivado integration failed") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        return {
            'version': self.vivado_version,
            'path': self.vivado_path,
            'board': self.board,
            'output_dir': str(self.output_dir)
        }


class VivadoIntegrationError(Exception):
    """Custom exception for Vivado integration errors."""
    pass
