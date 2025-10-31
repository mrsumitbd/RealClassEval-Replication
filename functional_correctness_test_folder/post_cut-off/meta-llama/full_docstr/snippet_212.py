
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


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
        self.vivado_version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        match = re.search(r'Vivado/(\d{4}\.\d)', path)
        if match:
            return match.group(1)
        else:
            raise VivadoIntegrationError(
                "Failed to extract Vivado version from path")

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        # Assuming we're using Docker, we'll use docker to run the command on the host
        # This requires Docker socket to be mounted inside the container
        try:
            subprocess.run(['docker', 'run', '--rm', '-v', f'{self.output_dir}:/output', '-v', '/var/run/docker.sock:/var/run/docker.sock',
                           'vivado_runner', 'vivado', '-mode', 'batch', '-source', '/output/run_vivado.tcl'])
        except subprocess.CalledProcessError as e:
            raise VivadoIntegrationError("Failed to run Vivado on host") from e

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
            try:
                vivado_cmd = f'{self.vivado_path}/bin/vivado -mode batch -source {self.output_dir}/run_vivado.tcl'
                subprocess.run(vivado_cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise VivadoIntegrationError("Failed to run Vivado") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        return {
            'version': self.vivado_version,
            'path': self.vivado_path,
        }
