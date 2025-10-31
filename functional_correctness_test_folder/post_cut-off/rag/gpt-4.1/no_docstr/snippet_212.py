
import os
import sys
import subprocess
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

    def __init__(
        self,
        board: str,
        output_dir: Path,
        vivado_path: str,
        logger: Optional[logging.Logger] = None,
        device_config: Optional[Dict[str, Any]] = None
    ):
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
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger("VivadoRunner")
        self.device_config = device_config or {}
        self.vivado_version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Typical Vivado path: /opt/Xilinx/Vivado/2022.2/bin/vivado
        # or /opt/Xilinx/Vivado/2022.2
        parts = Path(path).parts
        for i, part in enumerate(parts):
            if part.lower() == "vivado" and i+1 < len(parts):
                version = parts[i+1]
                if version[0].isdigit():
                    return version
        # fallback: try to find a version-like string
        for part in parts:
            if part[0].isdigit() and "." in part:
                return part
        return "unknown"

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        # Common heuristics: check for /.dockerenv or cgroup info
        if os.path.exists("/.dockerenv"):
            return True
        try:
            with open("/proc/1/cgroup", "rt") as f:
                content = f.read()
                if "docker" in content or "containerd" in content or "kubepods" in content:
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        self.logger.info(
            "Attempting to run Vivado on host system (not in container).")
        # This is a placeholder: in a real system, you might use a host-exec tool or SSH
        raise VivadoIntegrationError(
            "Running Vivado on host from container is not implemented.")

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self.logger.info(
                "Detected container environment. Will attempt to run Vivado on host.")
            self._run_vivado_on_host()
            return

        tcl_script = self.output_dir / "run_vivado.tcl"
        if not tcl_script.exists():
            raise VivadoIntegrationError(
                f"Vivado TCL script not found: {tcl_script}")

        vivado_bin = Path(self.vivado_path)
        if vivado_bin.is_dir():
            vivado_bin = vivado_bin / "bin" / "vivado"
        if not vivado_bin.exists():
            raise VivadoIntegrationError(
                f"Vivado binary not found at: {vivado_bin}")

        cmd = [
            str(vivado_bin),
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
            self.logger.debug("Vivado stdout:\n%s", result.stdout)
            if result.stderr:
                self.logger.debug("Vivado stderr:\n%s", result.stderr)
        except subprocess.CalledProcessError as e:
            self.logger.error(
                "Vivado failed with return code %d", e.returncode)
            self.logger.error("Vivado stdout:\n%s", e.stdout)
            self.logger.error("Vivado stderr:\n%s", e.stderr)
            raise VivadoIntegrationError(f"Vivado failed: {e.stderr}") from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info = {
            "vivado_path": str(self.vivado_path),
            "vivado_version": self.vivado_version,
            "board": self.board,
            "output_dir": str(self.output_dir),
        }
        vivado_bin = Path(self.vivado_path)
        if vivado_bin.is_dir():
            vivado_bin = vivado_bin / "bin" / "vivado"
        if vivado_bin.exists():
            try:
                result = subprocess.run(
                    [str(vivado_bin), "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                info["vivado_version_output"] = result.stdout.strip()
            except Exception as e:
                info["vivado_version_output"] = f"Error: {e}"
        else:
            info["vivado_version_output"] = "Vivado binary not found"
        return info
