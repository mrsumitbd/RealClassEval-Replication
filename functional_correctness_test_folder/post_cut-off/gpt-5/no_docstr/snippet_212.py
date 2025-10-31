import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


class VivadoRunner:
    def __init__(self, board: str, output_dir: Path, vivado_path: str, logger: Optional[logging.Logger] = None, device_config: Optional[Dict[str, Any]] = None):
        self.board = board
        self.output_dir = Path(output_dir)
        self.vivado_path = vivado_path
        self.device_config = device_config or {}

        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.vivado_version = self._extract_version_from_path(self.vivado_path)
        self.running_in_container = self._is_running_in_container()

    def _extract_version_from_path(self, path: str) -> str:
        p = Path(path)
        parts = list(p.parts)
        for part in reversed(parts):
            m = re.search(r"\b(\d{4}\.\d+|\d+\.\d+)\b", part)
            if m:
                return m.group(1)

        try:
            res = subprocess.run(
                [path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
            )
            if res.stdout:
                m = re.search(
                    r"Vivado.*?v?(\d{4}\.\d+|\d+\.\d+)", res.stdout, re.IGNORECASE)
                if m:
                    return m.group(1)
        except Exception:
            pass

        return "unknown"

    def _is_running_in_container(self) -> bool:
        if os.getenv("RUNNING_IN_CONTAINER", "").lower() in {"1", "true", "yes"}:
            return True
        try:
            if Path("/.dockerenv").exists():
                return True
        except Exception:
            pass
        try:
            cgroup = Path("/proc/1/cgroup")
            if cgroup.exists():
                data = cgroup.read_text(errors="ignore")
                if any(x in data for x in ("docker", "containerd", "kubepods", "podman")):
                    return True
        except Exception:
            pass
        return False

    def _run_vivado_on_host(self) -> None:
        exe = self.vivado_path
        log_file = self.output_dir / "vivado_run.log"

        if shutil.which(exe) is None and not Path(exe).is_file():
            msg = f"Vivado executable not found: {exe}"
            self.logger.error(msg)
            log_file.write_text(msg + "\n")
            return

        tcl_script = self.device_config.get("tcl_script")
        env = os.environ.copy()
        extra_args = self.device_config.get("args", [])
        if not isinstance(extra_args, (list, tuple)):
            extra_args = [str(extra_args)]

        if tcl_script:
            cmd = [exe, "-mode", "batch", "-source",
                   str(tcl_script), *map(str, extra_args)]
        else:
            cmd = [exe, "-version"]

        self.logger.info(f"Running Vivado command: {' '.join(map(str, cmd))}")
        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                cwd=self.output_dir,
                timeout=self.device_config.get("timeout", 600),
                check=False,
            )
            output = res.stdout or ""
            log_file.write_text(output)
            if res.returncode != 0:
                self.logger.error(
                    f"Vivado returned non-zero exit code: {res.returncode}")
            else:
                self.logger.info("Vivado executed successfully.")
        except subprocess.TimeoutExpired as e:
            self.logger.error("Vivado execution timed out.")
            log_file.write_text((e.stdout or "") + "\n[Timeout]\n")
        except Exception as e:
            self.logger.exception("Error while executing Vivado.")
            try:
                with log_file.open("a") as f:
                    f.write(f"\n[Exception] {e}\n")
            except Exception:
                pass

    def run(self) -> None:
        mode = "container" if self.running_in_container else "host"
        self.logger.info(
            f"Starting Vivado run for board '{self.board}' in {mode} mode.")
        self._run_vivado_on_host()

    def get_vivado_info(self) -> Dict[str, str]:
        info: Dict[str, str] = {
            "board": str(self.board),
            "vivado_path": str(self.vivado_path),
            "vivado_version": str(self.vivado_version),
            "output_dir": str(self.output_dir),
            "running_in_container": "true" if self.running_in_container else "false",
        }
        if "part" in self.device_config:
            info["device_part"] = str(self.device_config["part"])
        if "device" in self.device_config:
            info["device"] = str(self.device_config["device"])
        exists = shutil.which(self.vivado_path) is not None or Path(
            self.vivado_path).is_file()
        info["executable_found"] = "true" if exists else "false"
        return info
