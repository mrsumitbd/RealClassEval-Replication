
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #


class VivadoIntegrationError(RuntimeError):
    """Raised when Vivado integration fails."""


# --------------------------------------------------------------------------- #
# VivadoRunner
# --------------------------------------------------------------------------- #
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
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.vivado_path = Path(vivado_path).expanduser().resolve()
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Resolve Vivado binary
        self.vivado_bin = self.vivado_path / "bin" / "vivado"
        if not self.vivado_bin.is_file():
            raise VivadoIntegrationError(
                f"Vivado binary not found at {self.vivado_bin}"
            )

        # Extract version
        self.vivado_version = self._extract_version_from_path(
            str(self.vivado_path))

    # ----------------------------------------------------------------------- #
    # Helper methods
    # ----------------------------------------------------------------------- #
    def _extract_version_from_path(self, path: str) -> str:
        """Extract Vivado version from installation path."""
        # Common patterns: /opt/Xilinx/Vivado/2023.1, /opt/Xilinx/Vivado_2023.1
        match = re.search(r"Vivado[._-]?(\d{4}\.\d{1,2})", path, re.IGNORECASE)
        if match:
            return match.group(1)
        # Fallback: try to run vivado -version
        try:
            result = subprocess.run(
                [str(self.vivado_bin), "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            ver_match = re.search(r"Vivado\s+(\d{4}\.\d{1,2})", result.stdout)
            if ver_match:
                return ver_match.group(1)
        except Exception:
            pass
        return "unknown"

    def _is_running_in_container(self) -> bool:
        """Check if we're running inside a container."""
        # Common indicators of a container
        if os.path.exists("/.dockerenv"):
            return True
        if os.path.exists("/proc/1/cgroup"):
            with open("/proc/1/cgroup") as f:
                return "docker" in f.read() or "lxc" in f.read()
        # Environment variable sometimes set by CI
        return os.getenv("CONTAINER", "").lower() in ("true", "1", "yes")

    def _run_vivado_on_host(self) -> None:
        """Drop out of container and run Vivado on the host system."""
        self.logger.info(
            "Running Vivado on host system (container detected). "
            "Please ensure Vivado is installed and accessible on the host."
        )
        # In a real implementation we might use docker exec or similar.
        # Here we simply raise an error to indicate manual intervention.
        raise VivadoIntegrationError(
            "Running Vivado from within a container is not supported. "
            "Please run this script on the host machine."
        )

    # ----------------------------------------------------------------------- #
    # Public API
    # ----------------------------------------------------------------------- #
    def run(self) -> None:
        """
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.

        Raises:
            VivadoIntegrationError: If Vivado integration fails
        """
        if self._is_running_in_container():
            self._run_vivado_on_host()

        # Assume a TCL script named "run.tcl" exists in the output directory
        script_path = self.output_dir / "run.tcl"
        if not script_path.is_file():
            raise VivadoIntegrationError(
                f"TCL script not found: {script_path}. "
                "Please generate the Vivado project before running."
            )

        cmd = [
            str(self.vivado_bin),
            "-mode",
            "batch",
            "-notrace",
            "-nolog",
            "-nojournal",
            "-source",
            str(script_path),
        ]

        self.logger.info(f"Running Vivado: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            self.logger.debug("Vivado stdout:\n%s", result.stdout)
            self.logger.debug("Vivado stderr:\n%s", result.stderr)
        except subprocess.CalledProcessError as exc:
            self.logger.error(
                "Vivado failed with exit code %s", exc.returncode)
            self.logger.error("stdout:\n%s", exc.stdout)
            self.logger.error("stderr:\n%s", exc.stderr)
            raise VivadoIntegrationError(
                f"Viv
