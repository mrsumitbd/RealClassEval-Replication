
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


class VivadoRunner:
    """
    Minimal implementation of a Vivado runner.

    The class is intentionally lightweight – it only provides the
    functionality required by the tests that exercise the public API.
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
            Name of the target board.
        output_dir : Path
            Directory where Vivado will write its output.
        vivado_path : str
            Path to the Vivado executable or installation directory.
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

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _extract_version_from_path(self, path: str) -> str:
        """
        Extract a Vivado version string from a path.

        The function looks for a component that matches the pattern
        ``YYYY.Y`` (e.g. ``2023.1``).  If no such component is found,
        an empty string is returned.

        Parameters
        ----------
        path : str
            Path string to parse.

        Returns
        -------
        str
            Extracted version string or empty string.
        """
        import re

        # Split the path into components and search for a version pattern
        for part in Path(path).parts:
            match = re.match(r"(\d{4}\.\d+)", part)
            if match:
                return match.group(1)
        return ""

    def _is_running_in_container(self) -> bool:
        """
        Detect if the process is running inside a container.

        The detection is based on two heuristics:
        1. Presence of the file ``/.dockerenv``.
        2. The contents of ``/proc/1/cgroup`` containing the word
           ``docker`` or ``lxc``.
        """
        # Heuristic 1: /.dockerenv
        if Path("/.dockerenv").exists():
            return True

        # Heuristic 2: cgroup
        try:
            with open("/proc/1/cgroup", "r") as f:
                content = f.read()
                if "docker" in content or "lxc" in content:
                    return True
        except Exception:
            pass

        return False

    def _run_vivado_on_host(self) -> None:
        """
        Execute Vivado in the host environment.

        The method constructs a simple Vivado command that opens the
        project file located in ``output_dir`` and runs synthesis.
        Errors are logged and re‑raised as ``RuntimeError``.
        """
        # Build the Vivado command
        vivado_exe = self.vivado_path / "vivado"
        if not vivado_exe.exists():
            # If the path points to a directory, assume the executable is
            # inside it
            vivado_exe = self.vivado_path / "bin" / "vivado"

        if not vivado_exe.exists():
            raise RuntimeError(f"Vivado executable not found at {vivado_exe}")

        # Example TCL script that runs synthesis
        tcl_script = self.output_dir / "run_synth.tcl"
        tcl_script.write_text(
            f"""
            set board_name {self.board}
            create_project -name {self.board}_proj -part {self.device_config.get('part', 'unknown')} -force
            read_verilog {self.output_dir / "design.v"}
            synth_design -top top
            write_bitstream -force {self.output_dir / "design.bit"}
            exit
            """
        )

        cmd = [str(vivado_exe), "-mode", "batch", "-source", str(tcl_script)]
        self.logger.debug(f"Running Vivado command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            self.logger.info("Vivado finished successfully.")
            self.logger.debug(f"Vivado stdout:\n{result.stdout}")
            self.logger.debug(f"Vivado stderr:\n{result.stderr}")
        except subprocess.CalledProcessError as exc:
            self.logger.error(
                f"Vivado failed with return code {exc.returncode}")
            self.logger.error(f"stdout: {exc.stdout}")
            self.logger.error(f"stderr: {exc.stderr}")
            raise RuntimeError("Vivado execution failed") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> None:
        """
        Run the Vivado workflow.

        If the process is detected to be running inside a container,
        the method simply logs a warning and skips execution.  Otherwise,
        it delegates to ``_run_vivado_on_host``.
        """
        if self._is_running_in_container():
            self.logger.warning(
                "Detected container environment – Vivado execution is skipped."
            )
            return

        self.logger.info("Starting Vivado run.")
        self._run_vivado_on_host()
        self.logger.info("Vivado run completed.")

    def get_vivado_info(self) -> Dict[str, str]:
        """
        Return a dictionary containing basic Vivado information.

        The dictionary includes:
        - board
        - output_dir
        - vivado_path
        - device_config (stringified)
        - version (extracted from vivado_path)
        """
        version = self._extract_version_from_path(str(self.vivado_path))
        return {
            "board": self.board,
            "output_dir": str(self.output_dir),
            "vivado_path": str(self.vivado_path),
            "device_config": str(self.device_config),
            "version": version,
        }
