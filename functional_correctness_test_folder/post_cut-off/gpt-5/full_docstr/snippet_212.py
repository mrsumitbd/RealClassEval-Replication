import logging
import os
import re
import subprocess
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
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.vivado_path = str(vivado_path)
        self.device_config = device_config.copy() if device_config else {}

        if logger is None:
            logger = logging.getLogger("VivadoRunner")
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        self.logger = logger

        self.version = self._extract_version_from_path(self.vivado_path)
        self.vivado_binary = self._resolve_vivado_binary()

    def _resolve_vivado_binary(self) -> Path:
        is_windows = os.name == "nt"
        names = ["vivado.bat", "vivado.exe"] if is_windows else ["vivado"]
        candidates = []

        base = Path(self.vivado_path)

        for name in names:
            candidates.append(base / "bin" / name)
            if self.version:
                candidates.append(base / self.version / "bin" / name)
            candidates.append(base / "Vivado" /
                              (self.version or "") / "bin" / name)
            if self.version:
                candidates.append(Path("/opt/Xilinx/Vivado") /
                                  self.version / "bin" / name)

        seen = set()
        uniq_candidates = []
        for c in candidates:
            if c not in seen:
                uniq_candidates.append(c)
                seen.add(c)

        for c in uniq_candidates:
            if c.is_file():
                return c

        # Fallback to the first plausible default even if not found yet; existence will be checked later
        return uniq_candidates[0] if uniq_candidates else (base / "bin" / (names[0] if names else "vivado"))

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Common Vivado versions look like 2020.2, 2021.1, 2022.2, etc.
        m = re.search(r'(?P<ver>\d{4}\.\d+)', path)
        if m:
            return m.group("ver")
        # Fallback: generic x.y or x.y.z
        m = re.search(r'(?P<ver>\d+\.\d+(?:\.\d+)?)', path)
        return m.group("ver") if m else ""

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        if os.environ.get("RUNNING_IN_CONTAINER", "").lower() in ("1", "true", "yes"):
            return True
        for marker in ("/.dockerenv", "/run/.containerenv"):
            if os.path.exists(marker):
                return True
        try:
            with open("/proc/1/cgroup", "rt", encoding="utf-8", errors="ignore") as f:
                data = f.read()
                if any(tag in data for tag in ("docker", "lxc", "kubepods", "containerd")):
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        # Without a host-bridge utility, we cannot actually escape the container.
        # Provide a clear error with guidance.
        raise VivadoIntegrationError(
            "Vivado must run on the host system. Detected containerized environment. "
            "Please execute this step on the host or provide a host-bridge tool."
        )

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self.logger.info(
                "Detected container environment; attempting to run Vivado on host.")
            self._run_vivado_on_host()
            return

        bin_path = self.vivado_binary
        if not bin_path or not bin_path.exists():
            raise VivadoIntegrationError(
                f"Vivado binary not found at: {bin_path}")

        # Determine TCL script or commands
        tcl_script = self.device_config.get("tcl_script")
        tcl_commands = self.device_config.get("tcl_commands")
        args = [str(bin_path), "-mode", "batch",
                "-nolog", "-nojournal", "-notrace"]

        temp_script_path = None
        if tcl_script:
            tcl_script = Path(tcl_script)
            if not tcl_script.is_file():
                raise VivadoIntegrationError(
                    f"TCL script not found: {tcl_script}")
            args += ["-source", str(tcl_script)]
        elif tcl_commands:
            temp_script_path = self.output_dir / "vivado_runner_tmp.tcl"
            with open(temp_script_path, "w", encoding="utf-8") as f:
                f.write(str(tcl_commands))
            args += ["-source", str(temp_script_path)]
        else:
            # Fallback: print version as a smoke test
            args = [str(bin_path), "-version"]

        self.logger.info("Launching Vivado: %s", " ".join(args))
        try:
            proc = subprocess.run(
                args,
                cwd=str(self.output_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
        finally:
            if temp_script_path and temp_script_path.exists():
                try:
                    temp_script_path.unlink()
                except Exception:
                    pass

        self.logger.debug("Vivado stdout:\n%s", proc.stdout)
        if proc.returncode != 0:
            self.logger.error("Vivado stderr:\n%s", proc.stderr)
            raise VivadoIntegrationError(
                f"Vivado exited with code {proc.returncode}")

        self.logger.info("Vivado completed successfully.")

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info: Dict[str, str] = {}
        info["board"] = self.board
        info["install_path"] = str(self.vivado_path)
        info["version_from_path"] = self.version or ""
        info["binary"] = str(self.vivado_binary)
        info["binary_exists"] = str(self.vivado_binary.exists())
        info["in_container"] = str(self._is_running_in_container())

        # Try to get vivado -version if available
        if self.vivado_binary.exists():
            try:
                out = subprocess.run(
                    [str(self.vivado_binary), "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                    check=False,
                )
                if out.returncode == 0:
                    # Extract the first line with Vivado v
                    first_line = next(
                        (line for line in out.stdout.splitlines() if "Vivado" in line), "").strip()
                    info["version_reported"] = first_line
                else:
                    info["version_reported"] = ""
            except Exception:
                info["version_reported"] = ""
        else:
            info["version_reported"] = ""

        return info
