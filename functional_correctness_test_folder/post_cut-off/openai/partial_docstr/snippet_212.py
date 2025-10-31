
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
    Helper to run Vivado in batch mode, handling container vs host execution.
    """

    def __init__(
        self,
        board: str,
        output_dir: Path,
        vivado_path: str,
        logger: Optional[logging.Logger] = None,
        device_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Parameters
        ----------
        board : str
            Target board name.
        output_dir : Path
            Directory where Vivado output will be written.
        vivado_path : str
            Path to the Vivado executable or directory containing it.
        logger : Optional[logging.Logger]
            Logger instance. If None, a default logger is created.
        device_config : Optional[Dict[str, Any]]
            Optional device configuration dictionary.
        """
        self.board = board
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.vivado_path = Path(vivado_path).expanduser().resolve()
        self.logger = logger or logging.getLogger(__name__)
        self.device_config = device_config or {}

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Determine Vivado version
        self.vivado_version = self._extract_version_from_path(
            str(self.vivado_path))

    def _extract_version_from_path(self, path: str) -> str:
        """
        Extract Vivado version from a path string.
        Looks for patterns like 'vivado-2023.1' or 'vivado_2023_1'.
        """
        patterns = [
            r"vivado[-_](\d{4}\.\d{1,2})",
            r"vivado[-_](\d{4}_\d{1,2})",
            r"vivado[-_](\d{4}\.\d{1,2}\.\d{1,2})",
        ]
        for pat in patterns:
            m = re.search(pat, path, re.IGNORECASE)
            if m:
                return m.group(1).replace("_", ".")
        # Fallback: try to run vivado -version
        try:
            result = subprocess.run(
                [str(self.vivado_path), "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            m = re.search(r"Vivado\s+(\d{4}\.\d{1,2})", result.stdout)
            if m:
                return m.group(1)
        except Exception:
            pass
        return "unknown"

    def _is_running_in_container(self) -> bool:
        """
        Detect if the process is running inside a container.
        Checks common indicators such as the presence of /proc/1/cgroup
        containing 'docker' or 'lxc', or the environment variable
        'CONTAINER' set to 'true'.
        """
        if os.getenv("CONTAINER", "").lower() == "true":
            return True
        try:
            with open("/proc/1/cgroup", "r") as f:
                content = f.read()
                if "docker" in content or "lxc" in content or "kubepods" in content:
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        """
        Execute Vivado in batch mode on the host system.
        The script to run is expected to be located in the output directory
        as 'vivado_script.tcl'.
        """
        script_path = self.output_dir / "vivado_script.tcl"
        if not script_path.exists():
            raise VivadoIntegrationError(
                f"Vivado script not found: {script_path}"
            )

        cmd = [
            str(self.vivado_path),
            "-mode",
            "batch",
            "-source",
            str(script_path),
            "-log",
            str(self.output_dir / "vivado.log"),
            "-tclargs",
            self.board,
        ]

        self.logger.debug(f"Running Vivado command: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Vivado failed: {e.stderr}")
            raise VivadoIntegrationError(
                f"Vivado execution failed: {e.stderr}") from e

    def run(self) -> None:
        """
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises
        ------
        VivadoIntegrationError
            If Vivado integration fails.
        """
        if self._is_running_in_container():
            self.logger.info(
                "Detected container environment; delegating to host.")
            # In a real scenario we might use docker exec or similar.
            # Here we simply call the host runner directly.
            self._run_vivado_on_host()
        else:
            self.logger.info("Running Vivado directly.")
            self._run_vivado_on_host()

    def get_vivado_info(self) -> Dict[str, str]:
        """
        Retrieve basic Vivado information such as version and build date.
        Returns
        -------
        Dict[str, str]
            Dictionary containing 'version' and 'build_date'.
        """
        try:
            result = subprocess.run(
                [str(self.vivado_path), "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            version_match = re.search(r"Vivado\s+(\d{4}\.\d{1,2})", output)
            date_match = re.search(r"Build\s+(\d{4}-\d{2}-\d{2})", output)
            return {
                "version": version_match.group(1) if version_match else "unknown",
                "build_date": date_match.group(1) if date_match else "unknown",
            }
        except Exception as e:
            self.logger.error(f"Failed to get Vivado info: {e}")
            return {"version": "unknown", "build_date": "unknown"}
