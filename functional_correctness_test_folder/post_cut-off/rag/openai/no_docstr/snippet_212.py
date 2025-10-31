
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

# Simple exception for Vivado integration failures


class VivadoIntegrationError(RuntimeError):
    """Raised when Vivado integration fails."""


class VivadoRunner:
    """
    Handles everything Vivado SIMPLY
    Attributes:
        board: current target device
        output_dir: dir for generated vivado project
        vivado_path: root path to xilinx vivado installation (all paths derived from here)
        logger: attach a logger
    """

    def __init__(
        self,
        board: str,
        output_dir: Path,
        vivado_path: str,
        logger: Optional[logging.Logger] = None,
        device_config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize VivadoRunner with simplified configuration.
        Args:
            board: Target board name (e.g., "pcileech_35t325_x1")
            output_dir: Directory for generated Vivado project
            vivado_path: Root path to Xilinx Vivado installation
            logger: Optional logger instance
            device_config: Optional device configuration dictionary
        """
        self.board = board
        self.output_dir = output_dir
        self.vivado_path = Path(vivado_path).resolve()
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Extract Vivado version from path
        self.vivado_version = self._extract_version_from_path(
            str(self.vivado_path))

        self.logger.debug(
            "VivadoRunner initialized: board=%s, output_dir=%s, vivado_path=%s, vivado_version=%s",
            self.board,
            self.output_dir,
            self.vivado_path,
            self.vivado_version,
        )

    def _extract_version_from_path(self, path: str) -> str:
        """Extract Vivado version from installation path."""
        # Common patterns: /opt/Xilinx/Vivado/2023.1, /opt/Xilinx/Vivado_2023.1
        match = re.search(r"Vivado[_/]?(\d{4}\.\d{1,2})", path)
        if match:
            return match.group(1)
        # Fallback: look for a 4-digit year and optional minor
        match = re.search(r"(\d{4}\.\d{1,2})", path)
        if match:
            return match.group(1)
        self.logger.warning(
            "Could not extract Vivado version from path: %s", path)
        return "unknown"

    def _is_running_in_container(self) -> bool:
        """Check if we're running inside a container."""
        # Common indicators of a container environment
        if Path("/.dockerenv").exists():
            return True
        try:
            with open("/proc/1/cgroup", "r") as f:
                content = f.read()
                if "docker" in content or "lxc" in content:
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        """Drop out of container and run Vivado on the host system."""
        # In a real implementation, this might involve re-executing the script
        # on the host. Here we simply run Vivado directly.
        self.run()

    def run(self) -> None:
        """
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        """
        vivado_bin = self.vivado_path / "bin" / "vivado"
        if not vivado_bin.exists():
            raise VivadoIntegrationError(
                f"Vivado binary not found at {vivado_bin}")

        # Assume a TCL script named 'run.tcl' is generated in output_dir
        script_path = self.output_dir / "run.tcl"
        if not script_path.exists():
            raise VivadoIntegrationError(
                f"Vivado script not found at {script_path}")

        cmd = [str(vivado_bin), "-mode", "batch", "-source", str(script_path)]
        self.logger.info("Running Vivado: %s", " ".join(cmd))

        if self._is_running_in_container():
            self.logger.debug(
                "Detected container environment; delegating to host.")
            # In a real scenario, we might use docker exec or similar.
            # Here we just run the command directly.
            # This is a placeholder for container exit logic.
            pass

        try:
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            raise VivadoIntegrationError(
                f"Failed to start Vivado: {exc}") from exc

        if result.returncode != 0:
            self.logger.error("Vivado exited with code %s", result.returncode)
            self.logger.error("Stdout: %s", result.stdout)
            self.logger.error("Stderr
