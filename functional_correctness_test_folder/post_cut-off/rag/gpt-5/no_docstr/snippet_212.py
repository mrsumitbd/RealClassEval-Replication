import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class VivadoIntegrationError(RuntimeError):
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
        self.output_dir = Path(output_dir).absolute()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.vivado_path = str(vivado_path)
        self.vivado_root = Path(vivado_path).expanduser().resolve()

        self.logger = logger or logging.getLogger("VivadoRunner")
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(levelname)s] %(name)s: %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.device_config: Dict[str, Any] = device_config.copy(
        ) if device_config else {}

        self.version = self._extract_version_from_path(str(self.vivado_root))
        self.platform = sys.platform

        # Identify vivado executable and settings script candidates
        self.vivado_bin = self._discover_vivado_binary()
        self.settings_script = self._discover_settings_script()

        # discover tcl script to run
        self.tcl_script = self._discover_tcl_script()

        # wrapper to run vivado on host if in container
        self.host_wrapper = self.device_config.get("wrapper") or os.environ.get(
            "VIVADO_HOST_WRAPPER") or os.environ.get("HOST_VIVADO_WRAPPER")

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        p = Path(path)
        candidates = [p.name] + list(reversed([x.name for x in p.parents]))
        version_re = re.compile(r'(?P<ver>\d{4,}\.\d+(?:\.\d+)?)')
        for c in candidates:
            m = version_re.search(c)
            if m:
                return m.group('ver')

        # Fallback to vivado --version
        vivado_bin = self._discover_vivado_binary()
        if vivado_bin and Path(vivado_bin).exists():
            try:
                proc = subprocess.run([vivado_bin, "-version"], check=False,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                # Example: "Vivado v2020.2 (64-bit)"
                m = re.search(
                    r'Vivado v(?P<ver>\d{4,}\.\d+(?:\.\d+)?)', proc.stdout or "")
                if m:
                    return m.group('ver')
            except Exception:
                pass
        return ""

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        # Common heuristics
        if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
            return True
        try:
            with open("/proc/1/cgroup", "r", encoding="utf-8") as f:
                data = f.read()
            if any(x in data for x in ("docker", "kubepods", "containerd", "podman")):
                return True
        except Exception:
            pass
        return os.environ.get("RUNNING_IN_CONTAINER", "").lower() in ("1", "true", "yes")

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        if not self.host_wrapper:
            raise VivadoIntegrationError(
                "Running in container but no host wrapper provided. Set VIVADO_HOST_WRAPPER or pass device_config['wrapper'].")

        wrapper_path = shutil.which(self.host_wrapper) or self.host_wrapper
        if not shutil.which(wrapper_path) and not Path(wrapper_path).exists():
            raise VivadoIntegrationError(
                f"Host wrapper not found: {wrapper_path}")

        args: list[str] = [wrapper_path]
        # Pass basic context to wrapper; wrapper can choose to ignore these
        args += ["--vivado-path", str(self.vivado_root)]
        if self.version:
            args += ["--vivado-version", self.version]
        args += ["--project-dir", str(self.output_dir)]
        args += ["--board", self.board]
        if self.tcl_script:
            args += ["--tcl", str(self.tcl_script)]
        tcl_args = self.device_config.get("tcl_args")
        if tcl_args:
            if isinstance(tcl_args, (list, tuple)):
                args += ["--tcl-args",
                         " ".join(shlex.quote(str(x)) for x in tcl_args)]
            else:
                args += ["--tcl-args", str(tcl_args)]

        env = os.environ.copy()
        env.setdefault("XILINX_VIVADO", str(self.vivado_root))
        if self.version:
            env.setdefault("VIVADO_VERSION", self.version)

        self.logger.info(
            "Delegating Vivado execution to host wrapper: %s", wrapper_path)
        proc = subprocess.run(args, cwd=self.output_dir, env=env)
        if proc.returncode != 0:
            raise VivadoIntegrationError(
                f"Host wrapper failed with return code {proc.returncode}")

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if not self.tcl_script:
            raise VivadoIntegrationError(
                "No TCL script found to run. Provide device_config['tcl_script'] or place a TCL script in the output directory.")

        if self._is_running_in_container():
            self._run_vivado_on_host()
            return

        vivado_bin = self.vivado_bin or shutil.which("vivado")
        if not vivado_bin:
            raise VivadoIntegrationError(
                "Vivado executable not found. Check vivado_path or ensure Vivado is on PATH.")

        env = os.environ.copy()
        env.setdefault("XILINX_VIVADO", str(self.vivado_root))
        if self.version:
            env.setdefault("VIVADO_VERSION", self.version)

        # Ensure vivado bin is on PATH if not already
        bin_dir = str(Path(vivado_bin).parent)
        env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH','')}"

        cmd = [vivado_bin, "-mode", "batch", "-source", str(self.tcl_script)]
        tcl_args = self.device_config.get("tcl_args")
        if tcl_args:
            if isinstance(tcl_args, (list, tuple)):
                cmd += ["-tclargs"] + [str(x) for x in tcl_args]
            else:
                cmd += ["-tclargs", str(tcl_args)]

        self.logger.info("Running Vivado: %s", " ".join(
            shlex.quote(c) for c in cmd))
        try:
            proc = subprocess.run(cmd, cwd=self.output_dir, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError:
            raise VivadoIntegrationError(
                "Vivado executable not found or not executable.")
        except Exception as exc:
            raise VivadoIntegrationError(
                f"Failed to execute Vivado: {exc}") from exc

        if proc.stdout:
            self.logger.info(proc.stdout)

        if proc.returncode != 0:
            raise VivadoIntegrationError(
                f"Vivado failed with return code {proc.returncode}")

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info: Dict[str, str] = {}
        info["vivado_path"] = str(self.vivado_root)
        info["vivado_bin"] = str(self.vivado_bin or "")
        info["settings_script"] = str(self.settings_script or "")
        info["version"] = self.version or ""
        info["platform"] = self.platform
        info["board"] = self.board
        info["project_dir"] = str(self.output_dir)
        info["in_container"] = "true" if self._is_running_in_container() else "false"
        info["vivado_bin_exists"] = "true" if (
            self.vivado_bin and Path(self.vivado_bin).exists()) else "false"
        info["settings_script_exists"] = "true" if (
            self.settings_script and Path(self.settings_script).exists()) else "false"
        info["host_wrapper"] = str(self.host_wrapper or "")
        return info

    def _discover_vivado_binary(self) -> Optional[str]:
        # Candidate locations
        candidates = []

        # Absolute given vivado_path could be directly to bin directory or root
        root = self.vivado_root

        if sys.platform.startswith("win"):
            candidates += [
                root / "bin" / "vivado.bat",
                root / "bin" / "vivado.exe",
                root / "vivado.bat",
                root / "vivado.exe",
            ]
        else:
            candidates += [
                root / "bin" / "vivado",
                root / "vivado",
                root / "bin" / "unwrapped" / "vivado",
            ]

        for c in candidates:
            if c.exists():
                return str(c)

        which = shutil.which("vivado")
        if which:
            return which
        return None

    def _discover_settings_script(self) -> Optional[str]:
        root = self.vivado_root
        if sys.platform.startswith("win"):
            candidates = [root / "settings64.bat", root / "settings.bat"]
        else:
            candidates = [root / "settings64.sh", root / "settings.sh"]
        for c in candidates:
            if c.exists():
                return str(c)
        return None

    def _discover_tcl_script(self) -> Optional[Path]:
        # device_config can provide explicit path
        cfg_script = self.device_config.get("tcl_script")
        if cfg_script:
            p = Path(cfg_script)
            if not p.is_absolute():
                p = self.output_dir / p
            if p.exists():
                return p

        # Environment override
        env_script = os.environ.get("VIVADO_TCL_SCRIPT")
        if env_script:
            p = Path(env_script)
            if not p.is_absolute():
                p = self.output_dir / p
            if p.exists():
                return p

        # Common defaults in output_dir
        for name in ("build.tcl", "run.tcl", "project.tcl", "top.tcl"):
            p = self.output_dir / name
            if p.exists():
                return p

        return None
