
import os
import subprocess
import sys
import logging
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
        self.output_dir = Path(output_dir)
        self.vivado_path = str(vivado_path)
        self.logger = logger or logging.getLogger("VivadoRunner")
        self.device_config = device_config or {}
        self.vivado_bin = os.path.join(self.vivado_path, "bin", "vivado")
        self.vivado_version = self._extract_version_from_path(self.vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Typical path: /opt/Xilinx/Vivado/2022.2
        parts = os.path.normpath(path).split(os.sep)
        for i, part in enumerate(parts):
            if part.lower() == "vivado" and i + 1 < len(parts):
                return parts[i + 1]
        # fallback: try to find a version-like string
        for part in reversed(parts):
            if part.count('.') == 1 and all(x.isdigit() for x in part.replace('.', '')):
                return part
        return "unknown"

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        # Check for common container environment variables or files
        if os.path.exists('/.dockerenv'):
            return True
        if os.path.exists('/run/.containerenv'):
            return True
        if os.environ.get('container', '') != '':
            return True
        # Check cgroup for docker/lxc
        try:
            with open('/proc/1/cgroup', 'rt') as f:
                content = f.read()
                if 'docker' in content or 'kubepods' in content or 'lxc' in content:
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        self.logger.info(
            "Vivado cannot be run inside a container. Please run on the host system.")
        raise VivadoIntegrationError(
            "Vivado execution attempted inside a container. Please run on the host.")

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self._run_vivado_on_host()

        tcl_script = self.output_dir / "run_vivado.tcl"
        if not tcl_script.exists():
            self.logger.error(f"TCL script not found: {tcl_script}")
            raise VivadoIntegrationError(f"TCL script not found: {tcl_script}")

        cmd = [
            self.vivado_bin,
            "-mode", "batch",
            "-source", str(tcl_script)
        ]
        self.logger.info(f"Running Vivado: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.output_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            self.logger.info("Vivado run completed successfully.")
            self.logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Vivado failed: {e.stderr}")
            raise VivadoIntegrationError(f"Vivado failed: {e.stderr}") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info = {
            "vivado_path": self.vivado_path,
            "vivado_bin": self.vivado_bin,
            "vivado_version": self.vivado_version,
            "board": self.board,
            "output_dir": str(self.output_dir)
        }
        # Try to get Vivado version from the binary
        try:
            result = subprocess.run(
                [self.vivado_bin, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            info["vivado_version_output"] = result.stdout.strip()
        except Exception as e:
            info["vivado_version_output"] = f"Error: {e}"
        return info
