import os
import re
import sys
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class VivadoIntegrationError(Exception):
    pass


class VivadoRunner:
    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = Path(output_dir)
        self.vivado_path = vivado_path
        self.device_config = device_config or {}
        self.logger = logger or logging.getLogger(__name__)
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._vivado_exe = self._resolve_vivado_executable(vivado_path)
        self._vivado_version = self._extract_version_from_path(
            self._vivado_exe) if self._vivado_exe else ""

    def _resolve_vivado_executable(self, path: str) -> Optional[str]:
        p = Path(path)
        if p.is_dir():
            cand = p / "bin" / "vivado"
            if sys.platform.startswith("win"):
                cand = cand.with_suffix(".bat")
            if cand.exists() and os.access(str(cand), os.X_OK):
                return str(cand)
        if p.exists() and os.access(str(p), os.X_OK):
            return str(p)
        exe = shutil.which(path)
        return exe

    def _extract_version_from_path(self, path: str) -> str:
        if not path:
            return ""
        # Common Vivado install paths contain year.version (e.g., 2022.2 or 2023.1)
        m = re.search(r"(?P<ver>20\d{2}\.\d+)", path)
        if m:
            return m.group("ver")
        # Try invoking vivado -version as fallback (lightweight)
        try:
            out = subprocess.run([path, "-version"], stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True, timeout=10)
            vmatch = re.search(r"Vivado\s+v?(\d{4}\.\d+)", out.stdout or "")
            if vmatch:
                return vmatch.group(1)
        except Exception:
            pass
        return ""

    def _is_running_in_container(self) -> bool:
        # Standard heuristics
        if os.path.exists("/.dockerenv"):
            return True
        try:
            with open("/proc/1/cgroup", "r", encoding="utf-8") as f:
                data = f.read()
            if any(tok in data for tok in ("docker", "containerd", "kubepods", "podman")):
                return True
        except Exception:
            pass
        if os.environ.get("IN_CONTAINER", "").lower() in ("1", "true", "yes"):
            return True
        return False

    def _run_vivado_on_host(self) -> None:
        raise VivadoIntegrationError(
            "Vivado execution from container is not supported by this runner. Execute on host or provide a reachable Vivado binary inside the environment.")

    def run(self) -> None:
        # Determine TCL script to run
        tcl_candidates = [
            self.output_dir / "run.tcl",
            self.output_dir / "build.tcl",
            self.output_dir / "vivado.tcl",
        ]
        tcl_script = next((p for p in tcl_candidates if p.exists()), None)
        if tcl_script is None:
            # Fallback: any .tcl in directory
            for p in sorted(self.output_dir.glob("*.tcl")):
                tcl_script = p
                break
        if tcl_script is None:
            raise VivadoIntegrationError(
                f"No TCL script found in {self.output_dir}")

        if not self._vivado_exe:
            if self._is_running_in_container():
                self._run_vivado_on_host()
                return
            raise VivadoIntegrationError(
                "Vivado executable not found. Please provide a valid vivado_path or ensure it is on PATH.")

        log_file = self.output_dir / "vivado.log"
        journal_file = self.output_dir / "vivado.jou"

        cmd = [
            self._vivado_exe,
            "-mode",
            "batch",
            "-source",
            str(tcl_script),
            "-notrace",
            "-log",
            str(log_file),
            "-journal",
            str(journal_file),
        ]

        env = os.environ.copy()
        if self.board:
            env["TARGET_BOARD"] = self.board
        if self.device_config:
            for k, v in self.device_config.items():
                if isinstance(k, str) and isinstance(v, (str, int, float)):
                    env[str(k)] = str(v)

        self.logger.info("Launching Vivado: %s", " ".join(cmd))
        try:
            proc = subprocess.run(cmd, cwd=str(self.output_dir), env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
            # Always write combined stdout to a companion log for debugging
            (self.output_dir /
             "vivado_stdout.log").write_text(proc.stdout or "", encoding="utf-8")
            if proc.returncode != 0:
                raise VivadoIntegrationError(
                    f"Vivado failed with exit code {proc.returncode}. See {log_file} and vivado_stdout.log for details.")
        except FileNotFoundError as e:
            raise VivadoIntegrationError(
                f"Vivado executable not found: {self._vivado_exe}") from e
        except subprocess.SubprocessError as e:
            raise VivadoIntegrationError("Vivado execution failed") from e

    def get_vivado_info(self) -> Dict[str, str]:
        info: Dict[str, str] = {
            "board": self.board,
            "output_dir": str(self.output_dir),
            "vivado_path": self._vivado_exe or self.vivado_path,
            "vivado_version": self._vivado_version or "",
            "in_container": str(self._is_running_in_container()),
        }
        return info
