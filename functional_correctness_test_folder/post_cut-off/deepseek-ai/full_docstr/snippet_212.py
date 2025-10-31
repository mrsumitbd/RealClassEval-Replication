
import logging
from pathlib import Path
from typing import Optional, Dict, Any


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
        parts = Path(path).parts
        for part in parts:
            if part.startswith('Vivado_'):
                return part.split('_')[1]
        return 'unknown'

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        try:
            with open('/proc/1/cgroup', 'r') as f:
                return 'docker' in f.read() or 'lxc' in f.read()
        except:
            return False

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        raise NotImplementedError(
            "Running Vivado on host from container is not implemented yet.")

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
            raise NotImplementedError(
                "Running Vivado in batch mode is not implemented yet.")

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        return {
            'version': self._extract_version_from_path(self.vivado_path),
            'path': self.vivado_path,
            'board': self.board,
        }
