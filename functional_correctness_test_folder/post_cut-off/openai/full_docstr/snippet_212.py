
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


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

        # Determine Vivado executable
        self.vivado_exe = self.vivado_path / "bin" / "vivado"
        if not self.vivado_exe.exists():
            raise VivadoIntegrationError(
                f"Vivado executable not found at {self.vivado_exe}"
            )

        # Extract version for logging
        self.version = self._extract_version_from_path(str(self.vivado_path))
        self.logger.debug(
            f"VivadoRunner initialized: board={self.board}, "
            f"output_dir={self.output_dir}, vivado_path={self.vivado_path}, "
            f"version={self.version}"
        )

    def _extract_version_from_path(self, path: str) -> str:
        """Extract Vivado version from installation path."""
        # Common pattern: /opt/Xilinx/Vivado/2023.1
        match = re.search(r"Vivado[\\/](\d{4}\.\d{1,2})", path)
        if match:
            return match.group(1)
        # Fallback: use basename
        return Path(path).name

    def _is_running_in_container(self) -> bool:
        """Check if we're running inside a container."""
        # Common indicators: /.dockerenv file or environment variable
        if Path("/.dockerenv").exists():
            return True
        if os.getenv("CONTAINER") == "true":
            return True
        return False

    def _run_vivado_on_host(self) -> None:
        """Drop out of container and run Vivado on the host system."""
        # This is a placeholder: in real usage, you might use docker exec or
        # a host script. Here we simply log the action.
        self.logger.info(
            "Running Vivado on host system (outside container). "
            f"Vivado path: {self.vivado_path}"
        )
        # Example: call host vivado via subprocess
        cmd = [str(self.vivado_exe), "-mode", "batch", "-source", "run.tcl"]
        self.logger.debug(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=self.output_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            self.logger.error(f"Vivado failed: {result.stderr}")
            raise VivadoIntegrationError("Vivado execution failed on host.")
        self.logger.info(f"Vivado output: {result.stdout}")

    def run(self) -> None:
        """
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        """
        self.logger.info("Starting Vivado run.")
        if self._is_running_in_container():
            self.logger.debug("Detected container environment.")
            self._run_vivado_on_host()
        else:
            # Run Vivado directly
            cmd = [str(self.vivado_exe), "-mode",
                   "batch", "-source", "run.tcl"]
            self.logger.debug(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.logger.error(f"Vivado failed: {result.stderr}")
                raise VivadoIntegrationError("Vivado execution failed.")
            self.logger.info(f"Vivado output: {result.stdout}")

    def get_vivado_info(self) -> Dict[str, str]:
        """Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        """
        self.logger.debug("Retrieving Vivado information.")
        cmd = [str(self.vivado_exe), "-version"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            # Example output: "Vivado v2023.1 (64-bit)\n..."
            match = re.search(r"Vivado v(\d{4}\.\d{1,2})", output)
            version = match.group(1) if match else "unknown"
            return {
                "vivado_path": str(self.vivado_path),
                "version": version,
                "full_output": output,
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get Vivado info: {e}")
            raise VivadoIntegrationError(
                "Could not retrieve Vivado info.") from e
