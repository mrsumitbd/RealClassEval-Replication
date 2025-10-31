
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
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.vivado_path = Path(vivado_path).expanduser().resolve()
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

        # Resolve the actual vivado executable
        self.vivado_exe = self.vivado_path / "bin" / "vivado"
        if not self.vivado_exe.exists():
            raise VivadoIntegrationError(
                f"Vivado executable not found at {self.vivado_exe}"
            )

        # Store version
        self.version = self._extract_version_from_path(str(self.vivado_path))

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    def _extract_version_from_path(self, path: str) -> str:
        """Extract Vivado version from installation path."""
        # Typical path: /opt/Xilinx/Vivado/2023.1
        match = re.search(r"Vivado[\\/](\d{4}\.\d{1,2})", path)
        if match:
            return match.group(1)
        # Fallback: try to run vivado -version
        try:
            out = subprocess.check_output(
                [str(self.vivado_exe), "-version"], stderr=subprocess.STDOUT
            ).decode()
            ver_match = re.search(r"Vivado ([\d\.]+)", out)
            if ver_match:
                return ver_match.group(1)
        except Exception:
            pass
        return "unknown"

    def _is_running_in_container(self) -> bool:
        """Check if we're running inside a container."""
        # Common indicator for Docker containers
        if os.path.exists("/.dockerenv"):
            return True
        # Check cgroup for container markers
        try:
            with open("/proc/1/cgroup", "r") as f:
                return any("docker" in line or "lxc" in line for line in f)
        except Exception:
            return False

    def _run_vivado_on_host(self) -> None:
        """Drop out of container and run Vivado on the host system."""
        # In a real implementation this would involve SSH or a host‑side
        # wrapper.  For the purposes of this simplified runner we simply
        # execute Vivado directly, assuming the host environment has the
        # same executable path.
        script_path = self.output_dir / "run.tcl"
        if not script_path.exists():
            raise VivadoIntegrationError(
                f"Vivado script not found: {script_path}"
            )
        cmd = [
            str(self.vivado_exe),
            "-mode",
            "batch",
            "-source",
            str(script_path),
        ]
        self.logger.debug("Running Vivado on host: %s", " ".join(cmd))
        try:
            subprocess.run(cmd, check=True, cwd=self.output_dir)
        except subprocess.CalledProcessError as exc:
            raise VivadoIntegrationError(
                f"Vivado failed on host: {exc}"
            ) from exc

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def run(self) -> None:
        """
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.

        Raises:
            VivadoIntegrationError: If Vivado integration fails
        """
        script_path = self.output_dir / "run.tcl"
        if not script_path.exists():
            raise VivadoIntegrationError(
                f"Vivado script not found: {script_path}"
            )

        cmd = [
            str(self.vivado_exe),
            "-mode",
            "batch",
            "-source",
            str(script_path),
        ]

        if self._is_running_in_container():
            self.logger.info(
                "Detected container environment; delegating to host.")
            self._run_vivado_on_host()
        else:
            self.logger.info("Running Vivado directly.")
            try:
                subprocess.run(cmd, check=True, cwd=self.output_dir)
            except subprocess.CalledProcessError as exc:
                raise VivadoIntegrationError(
                    f"Vivado failed: {exc}"
                ) from exc

    def get_vivado_info(self) -> Dict[str, str]:
        """Get information about the Vivado installation.

        Returns:
            Dictionary with Vivado installation details
        """
        info: Dict[str, str] = {}
        info["vivado_path"] = str(self.vivado_exe)
