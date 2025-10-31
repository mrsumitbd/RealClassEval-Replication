
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

        # Create a temporary script to run on the host
        host_script = self.output_dir / "run_vivado_on_host.sh"
        with host_script.open('w') as f:
            f.write("#!/bin/bash\n")
            f.write(f"cd {self.output_dir}\n")
            f.write(
                f"{self.vivado_path}/bin/vivado -mode batch -source {self.output_dir}/vivado_script.tcl\n")

        # Make the script executable
        host_script.chmod(0o755)

        # Use docker to run the script on the host
        try:
            subprocess.run([
                "docker", "run", "--rm", "--privileged",
                "-v", f"{self.output_dir}:/project",
                "-v", f"{self.vivado_path}:/vivado",
                "alpine", "/bin/sh", "-c",
                f"chroot /project /vivado/bin/vivado -mode batch -source /project/vivado_script.tcl"
            ], check=True)
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
        self.logger.info(
            f"Starting Vivado integration for board: {self.board}")

        # Generate the Vivado script
        vivado_script = self.output_dir / "vivado_script.tcl"
        with vivado_script.open('w') as f:
            f.write(
                f"create_project -force {self.board}_project {self.output_dir}\n")
            f.write(
                f"set_property board_part {self.board} [current_project]\n")
            # Add more Vivado commands as needed

        # Run Vivado
        try:
            if self._is_running_in_container():
                self._run_vivado_on_host()
            else:
                subprocess.run([
                    f"{self.vivado_path}/bin/vivado",
                    "-mode", "batch",
                    "-source", str(vivado_script)
                ], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Vivado integration failed: {e}")
            raise VivadoIntegrationError(f"Vivado integration failed: {e}")

        self.logger.info("Vivado integration completed successfully")

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
