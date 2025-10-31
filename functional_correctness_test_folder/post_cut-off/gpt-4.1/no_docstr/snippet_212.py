
import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any


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
            if part.lower() == "vivado" and i + 1 < len(parts):
                version = parts[i + 1]
                if any(c.isdigit() for c in version):
                    return version
        # Fallback: try to find a version-like string in the path
        for part in parts:
            if any(c.isdigit() for c in part) and '.' in part:
                return part
        return "unknown"

    def _is_running_in_container(self) -> bool:
        # Check for common container environment variables or files
        if os.path.exists('/.dockerenv'):
            return True
        if os.path.exists('/run/.containerenv'):
            return True
        cgroup_path = '/proc/1/cgroup'
        if os.path.isfile(cgroup_path):
            with open(cgroup_path, 'rt') as f:
                content = f.read()
                if 'docker' in content or 'kubepods' in content or 'containerd' in content:
                    return True
        return False

    def _run_vivado_on_host(self) -> None:
        tcl_script = self.output_dir / "run_vivado.tcl"
        if not tcl_script.exists():
            raise FileNotFoundError(f"TCL script not found: {tcl_script}")
        cmd = [
            self.vivado_path,
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
            self.logger.info(f"Vivado output:\n{result.stdout}")
            if result.stderr:
                self.logger.warning(f"Vivado errors:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Vivado failed with return code {e.returncode}")
            self.logger.error(f"stdout:\n{e.stdout}")
            self.logger.error(f"stderr:\n{e.stderr}")
            raise

    def run(self) -> None:
        self.logger.info(f"Starting Vivado run for board: {self.board}")
        if self._is_running_in_container():
            self.logger.info("Detected running inside a container.")
        else:
            self.logger.info("Running on host system.")
        self._run_vivado_on_host()
        self.logger.info("Vivado run completed.")

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
