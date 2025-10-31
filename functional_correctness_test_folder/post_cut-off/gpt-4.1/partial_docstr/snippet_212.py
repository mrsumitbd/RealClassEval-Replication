
import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any


class VivadoIntegrationError(Exception):
    pass


class VivadoRunner:

    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = vivado_path
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}
        self.vivado_version = self._extract_version_from_path(vivado_path)

    def _extract_version_from_path(self, path: str) -> str:
        # Try to extract version from path, e.g., /opt/Xilinx/Vivado/2022.1/bin/vivado
        parts = Path(path).parts
        for i, part in enumerate(parts):
            if part.lower() == "vivado" and i+1 < len(parts):
                version = parts[i+1]
                if any(c.isdigit() for c in version):
                    return version
        # fallback: try to extract version from the vivado binary itself
        try:
            result = subprocess.run(
                [path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            for line in result.stdout.splitlines():
                if "Vivado" in line and "version" in line.lower():
                    # e.g., "Vivado v2022.1 (64-bit)"
                    tokens = line.split()
                    for token in tokens:
                        if token.startswith('v') and any(c.isdigit() for c in token):
                            return token.lstrip('v')
        except Exception:
            pass
        return "unknown"

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        # Check for common container environment markers
        if os.path.exists('/.dockerenv'):
            return True
        try:
            with open('/proc/1/cgroup', 'rt') as f:
                content = f.read()
                if 'docker' in content or 'kubepods' in content or 'containerd' in content or 'lxc' in content:
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        # This is a placeholder for host execution logic.
        # In a real system, this might use a host-bridge or similar mechanism.
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
                "Detected container environment. Attempting to run Vivado on host.")
            self._run_vivado_on_host()
            return

        tcl_script = self.output_dir / "run_vivado.tcl"
        if not tcl_script.exists():
            raise VivadoIntegrationError(f"TCL script not found: {tcl_script}")
        cmd = [self.vivado_path, "-mode", "batch", "-source", str(tcl_script)]
        self.logger.info(f"Running Vivado: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, cwd=str(
                self.output_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.logger.debug(f"Vivado stdout:\n{result.stdout}")
            self.logger.debug(f"Vivado stderr:\n{result.stderr}")
            if result.returncode != 0:
                raise VivadoIntegrationError(
                    f"Vivado failed with return code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}")
        except Exception as e:
            raise VivadoIntegrationError(f"Failed to run Vivado: {e}")

    def get_vivado_info(self) -> Dict[str, str]:
        info = {
            "vivado_path": self.vivado_path,
            "vivado_version": self.vivado_version,
            "board": self.board,
            "output_dir": str(self.output_dir),
        }
        if self.device_config:
            info.update({f"device_{k}": str(v)
                        for k, v in self.device_config.items()})
        return info
