
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):

        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

    def _extract_version_from_path(self, path: str) -> str:

        version = path.split('/')[-1].split('-')[-1]
        return version

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''

        return os.path.exists('/.dockerenv')

    def _run_vivado_on_host(self) -> None:

        pass

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
            pass

    def get_vivado_info(self) -> Dict[str, str]:

        vivado_info = {
            'board': self.board,
            'output_dir': str(self.output_dir),
            'vivado_path': self.vivado_path,
            'version': self._extract_version_from_path(self.vivado_path)
        }
        return vivado_info
