
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any


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

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        version_file = Path(path) / 'VERSION.txt'
        if version_file.exists():
            with version_file.open('r') as f:
                return f.read().strip()
        return "unknown"

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        if not self._is_running_in_container():
            return

        self.logger.info(
            "Running in container, dropping out to host for Vivado execution")
        try:
            # This is a simplified approach - in a real implementation you might need
            # more sophisticated container escape mechanisms
            subprocess.run(["docker", "run", "--rm", "-v", f"{self.vivado_path}:/vivado",
                            "-v", f"{self.output_dir}:/output", "vivado-container",
                            "vivado", "-mode", "batch", "-source", "/output/run.tcl"],
                           check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to run Vivado on host: {e}")
            raise

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        try:
            if self._is_running_in_container():
                self._run_vivado_on_host()
            else:
                vivado_executable = Path(self.vivado_path) / "bin" / "vivado"
                if not vivado_executable.exists():
                    raise FileNotFoundError(
                        f"Vivado executable not found at {vivado_executable}")

                tcl_script = self.output_dir / "run.tcl"
                if not tcl_script.exists():
                    raise FileNotFoundError(
                        f"TCL script not found at {tcl_script}")

                self.logger.info(
                    f"Running Vivado in batch mode with script: {tcl_script}")
                subprocess.run([str(vivado_executable), "-mode", "batch", "-source", str(tcl_script)],
                               cwd=str(self.output_dir), check=True)
        except Exception as e:
            self.logger.error(f"Vivado execution failed: {e}")
            raise VivadoIntegrationError(
                f"Vivado integration failed: {e}") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        return {
            "version": self._extract_version_from_path(self.vivado_path),
            "path": self.vivado_path,
            "board": self.board,
            "output_dir": str(self.output_dir)
        }


class VivadoIntegrationError(Exception):
    '''Custom exception for Vivado integration errors.'''
    pass
