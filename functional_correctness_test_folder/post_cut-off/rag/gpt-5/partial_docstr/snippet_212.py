import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


try:
    from .exceptions import VivadoIntegrationError  # type: ignore
except Exception:
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
        self.vivado_path = str(vivado_path)
        self.device_config = device_config or {}

        if logger is None:
            logger = logging.getLogger('VivadoRunner')
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        self.logger = logger

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.vivado_root = Path(self.vivado_path).resolve()
        self.vivado_version = self._extract_version_from_path(self.vivado_path)

        # Determine vivado executable
        if sys.platform.startswith('win'):
            candidates = ['vivado.bat', 'vivado.exe']
        else:
            candidates = ['vivado']
        self.vivado_bin = None
        for c in candidates:
            candidate_path = self.vivado_root / 'bin' / c
            if candidate_path.exists():
                self.vivado_bin = candidate_path
                break
        if self.vivado_bin is None:
            which_vivado = shutil.which('vivado')
            if which_vivado:
                self.vivado_bin = Path(which_vivado)
        if self.vivado_bin is None:
            self.logger.debug(
                'Vivado not found at %s/bin or in PATH', self.vivado_root)
        else:
            self.logger.debug('Using Vivado executable: %s', self.vivado_bin)

        # Cache probable script candidates
        self._script_candidates = [
            self.output_dir / 'run.tcl',
            self.output_dir / 'build.tcl',
            self.output_dir / 'project.tcl',
            self.output_dir / 'vivado_run.tcl',
        ]

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Match .../Vivado/2023.1/... or ...\Vivado\2023.1\...
        m = re.search(r'(?:^|[\\/])Vivado[\\/](\d{4}\.\d+)(?:[\\/]|$)', path)
        if m:
            return m.group(1)
        # Try to extract from path like .../Xilinx/2023.2/Vivado/...
        m = re.search(
            r'(?:^|[\\/])(\d{4}\.\d+)(?:[\\/])Vivado(?:[\\/]|$)', path)
        if m:
            return m.group(1)
        return 'unknown'

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        if os.path.exists('/.dockerenv'):
            return True
        try:
            with open('/proc/1/cgroup', 'rt', encoding='utf-8') as f:
                data = f.read()
            if any(token in data for token in ('docker', 'kubepods', 'containerd', 'podman')):
                return True
        except Exception:
            pass
        if os.getenv('RUNNING_IN_CONTAINER') or os.getenv('IN_DOCKER') or os.getenv('IN_CONTAINER'):
            return True
        return False

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        host_runner = os.getenv('VIVADO_HOST_RUNNER')
        if not host_runner:
            raise VivadoIntegrationError(
                'VIVADO_HOST_RUNNER not set; cannot delegate Vivado execution to host.')

        script = self._select_tcl_script()
        if not script:
            raise VivadoIntegrationError(
                'No Vivado TCL script found to execute on host.')

        cmd = [host_runner, 'vivado', '-mode', 'batch', '-nolog',
               '-nojournal', '-notrace', '-source', str(script)]
        tclargs = self._build_tclargs()
        if tclargs:
            cmd.extend(['-tclargs'] + tclargs)

        self.logger.info(
            'Delegating Vivado execution to host: %s', ' '.join(cmd))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise VivadoIntegrationError(
                f'Vivado host execution failed with exit code {e.returncode}') from e
        except FileNotFoundError as e:
            raise VivadoIntegrationError(
                f'Host runner not found: {host_runner}') from e

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        if self._is_running_in_container():
            self.logger.info('Detected container environment.')
            try:
                self._run_vivado_on_host()
                return
            except VivadoIntegrationError as e:
                self.logger.warning(
                    'Failed to delegate to host: %s. Attempting in-container run...', e)

        script = self._select_tcl_script()
        if not script:
            raise VivadoIntegrationError(
                'No Vivado TCL script found in output directory.')

        vivado_exec = self._resolve_vivado_executable()
        if not vivado_exec:
            raise VivadoIntegrationError(
                'Vivado executable not found. Ensure Vivado is installed and available in PATH or vivado_path is correct.')

        env = os.environ.copy()
        env.setdefault('XILINX_VIVADO', str(self.vivado_root))
        env['PATH'] = str(self.vivado_root / 'bin') + \
            os.pathsep + env.get('PATH', '')

        cmd = [str(vivado_exec), '-mode', 'batch', '-nolog',
               '-nojournal', '-notrace', '-source', str(script)]
        tclargs = self._build_tclargs()
        if tclargs:
            cmd.extend(['-tclargs'] + tclargs)

        self.logger.info('Running Vivado: %s', ' '.join(cmd))
        try:
            subprocess.run(cmd, check=True, cwd=str(self.output_dir), env=env)
        except subprocess.CalledProcessError as e:
            raise VivadoIntegrationError(
                f'Vivado run failed with exit code {e.returncode}') from e
        except FileNotFoundError as e:
            raise VivadoIntegrationError(
                f'Vivado executable not found: {vivado_exec}') from e

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info: Dict[str, str] = {
            'board': self.board,
            'output_dir': str(self.output_dir),
            'vivado_root': str(self.vivado_root),
            'vivado_bin': str(self.vivado_bin) if self.vivado_bin else '',
            'version_path': self.vivado_version,
            'in_container': str(self._is_running_in_container()),
        }

        # Try to query vivado -version if available
        vivado_exec = self._resolve_vivado_executable(allow_none=True)
        if vivado_exec:
            try:
                out = subprocess.run([str(vivado_exec), '-version'], check=False,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
                info['vivado_version_output'] = out.stdout.strip()
                m = re.search(r'Vivado v?(\d{4}\.\d+)', out.stdout)
                if m:
                    info['version_detected'] = m.group(1)
            except Exception:
                pass

        return info

    def _select_tcl_script(self) -> Optional[Path]:
        for s in self._script_candidates:
            if s.exists():
                return s
        # Fallback: any .tcl in output_dir
        for s in sorted(self.output_dir.glob('*.tcl')):
            return s
        return None

    def _resolve_vivado_executable(self, allow_none: bool = False) -> Optional[Path]:
        if self.vivado_bin and self.vivado_bin.exists():
            return self.vivado_bin
        which_vivado = shutil.which('vivado')
        if which_vivado:
            return Path(which_vivado)
        return None if allow_none else self.vivado_bin

    def _build_tclargs(self) -> list[str]:
        args: list[str] = []
        # Always pass board and output_dir as first args
        args.extend(['board', self.board, 'outdir', str(self.output_dir)])
        # Add device_config as key=value pairs
        for k, v in self.device_config.items():
            args.extend([str(k), str(v)])
        return args
