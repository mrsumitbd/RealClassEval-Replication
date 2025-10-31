import logging
import os
import platform
import re
import shlex
import shutil
import subprocess
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
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.vivado_root = Path(vivado_path).resolve()
        self.vivado_path = str(self.vivado_root)

        self.device_config: Dict[str, Any] = device_config.copy(
        ) if device_config else {}

        if logger is None:
            logger = logging.getLogger('VivadoRunner')
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s %(levelname)s %(name)s: %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        self.logger = logger

        self.version = self._extract_version_from_path(self.vivado_path)
        is_windows = platform.system().lower().startswith('win')

        self.vivado_bin = (self.vivado_root / 'bin' /
                           ('vivado.bat' if is_windows else 'vivado')).resolve()
        self.settings_script = (
            self.vivado_root / ('settings64.bat' if is_windows else 'settings64.sh')).resolve()
        self.is_windows = is_windows

        # Prepare environment
        self.env = os.environ.copy()
        self.env.setdefault('XILINX_VIVADO', str(self.vivado_root))
        if self.version:
            self.env.setdefault('VIVADO_VERSION', self.version)

    def _extract_version_from_path(self, path: str) -> str:
        '''Extract Vivado version from installation path.'''
        # Common structures: /opt/Xilinx/Vivado/2022.2, C:\Xilinx\Vivado\2020.2
        m = re.search(
            r'[\\/]Vivado[\\/]([0-9]{4}\.[0-9]+)', path, flags=re.IGNORECASE)
        if m:
            return m.group(1)
        # Fallback to first X.Y pattern
        m = re.search(r'([0-9]{4}\.[0-9]+)', path)
        if m:
            return m.group(1)
        m = re.search(r'([0-9]+\.[0-9]+)', path)
        return m.group(1) if m else ''

    def _is_running_in_container(self) -> bool:
        '''Check if we're running inside a container.'''
        try:
            if os.path.exists('/.dockerenv'):
                return True
            # podman/containers often expose container envs
            for key in ('IN_CONTAINER', 'RUNNING_IN_CONTAINER', 'CONTAINER', 'DOCKER_CONTAINER'):
                if os.environ.get(key, '').strip().lower() in ('1', 'true', 'yes'):
                    return True
            # Check cgroup identifiers for containerization
            cgroup_path = '/proc/1/cgroup'
            if os.path.exists(cgroup_path):
                with open(cgroup_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                    if re.search(r'docker|kubepods|containerd|podman|lxc', data, flags=re.IGNORECASE):
                        return True
        except Exception:
            pass
        return False

    def _build_vivado_batch_command(self, tcl_script: Path) -> list[str]:
        # Build the command to execute vivado in batch mode; source settings if present
        vivado_cmd = f'"{self.vivado_bin}" -mode batch -nojournal -nolog -notrace -source "{tcl_script}"'
        if self.is_windows:
            if self.settings_script.exists():
                return ['cmd.exe', '/c', f'"{self.settings_script}" && {vivado_cmd}']
            return ['cmd.exe', '/c', vivado_cmd]
        # POSIX
        if self.settings_script.exists():
            # Use bash login shell to source settings then run vivado
            return ['/usr/bin/env', 'bash', '-lc', f'source "{self.settings_script}" >/dev/null 2>&1 && {vivado_cmd}']
        return ['/usr/bin/env', 'bash', '-lc', vivado_cmd]

    def _run_vivado_on_host(self) -> None:
        '''Drop out of container and run Vivado on the host system.'''
        # Build the vivado command
        tcl_script = self.output_dir / 'run.tcl'
        cmd = self._build_vivado_batch_command(tcl_script)

        # Try user-specified host bridge command first
        host_cmd_env = os.environ.get('VIVADO_HOST_CMD', '').strip()
        if host_cmd_env:
            bridge = shlex.split(host_cmd_env)
            final_cmd = bridge + cmd
            self.logger.info(
                'Running Vivado on host via VIVADO_HOST_CMD: %s', ' '.join(final_cmd))
            subprocess.run(final_cmd, check=True, env=self.env,
                           cwd=str(self.output_dir))
            return

        # Try host-spawn, a common tool to execute commands on host from containers
        host_spawn = shutil.which('host-spawn')
        if host_spawn:
            final_cmd = [host_spawn] + cmd
            self.logger.info(
                'Running Vivado on host via host-spawn: %s', ' '.join(final_cmd))
            subprocess.run(final_cmd, check=True, env=self.env,
                           cwd=str(self.output_dir))
            return

        # Try nsenter into PID 1 namespaces if permitted
        nsenter = shutil.which('nsenter')
        if nsenter and os.geteuid() == 0:
            final_cmd = [nsenter, '-t', '1', '-m',
                         '-u', '-i', '-n', '-p', '--'] + cmd
            self.logger.info(
                'Running Vivado on host via nsenter: %s', ' '.join(final_cmd))
            subprocess.run(final_cmd, check=True, env=self.env,
                           cwd=str(self.output_dir))
            return

        raise VivadoIntegrationError(
            'Unable to execute Vivado on host: set VIVADO_HOST_CMD, install host-spawn, or allow nsenter.')

    def run(self) -> None:
        '''
        Hand-off to Vivado in batch mode using the generated scripts.
        If running in container, drop out to host for Vivado execution.
        Raises:
            VivadoIntegrationError: If Vivado integration fails
        '''
        try:
            # Ensure a tcl exists; create a minimal no-op if missing
            tcl_script = self.output_dir / 'run.tcl'
            if not tcl_script.exists():
                tcl_script.write_text(
                    'puts "Vivado batch placeholder for board: %s"\nexit 0\n' % self.board,
                    encoding='utf-8'
                )

            if self._is_running_in_container():
                self.logger.info(
                    'Detected containerized environment; delegating Vivado execution to host.')
                self._run_vivado_on_host()
                return

            # Local execution
            cmd = self._build_vivado_batch_command(tcl_script)
            if not self.vivado_bin.exists() and not shutil.which('vivado'):
                raise VivadoIntegrationError(
                    f'Vivado executable not found at {self.vivado_bin} and not in PATH.')

            self.logger.info('Executing Vivado: %s', ' '.join(cmd))
            subprocess.run(cmd, check=True, env=self.env,
                           cwd=str(self.output_dir))
        except subprocess.CalledProcessError as exc:
            raise VivadoIntegrationError(
                f'Vivado execution failed with exit code {exc.returncode}') from exc
        except FileNotFoundError as exc:
            raise VivadoIntegrationError(
                f'Vivado or required tools not found: {exc}') from exc

    def get_vivado_info(self) -> Dict[str, str]:
        '''Get information about the Vivado installation.
        Returns:
            Dictionary with Vivado installation details
        '''
        info: Dict[str, str] = {}
        info['install_root'] = str(self.vivado_root)
        info['vivado_bin'] = str(self.vivado_bin)
        info['settings_script'] = str(self.settings_script)
        info['version_from_path'] = self.version or ''
        info['board'] = self.board
        info['output_dir'] = str(self.output_dir)
        info['in_container'] = 'true' if self._is_running_in_container() else 'false'
        info['host_cmd'] = os.environ.get('VIVADO_HOST_CMD', '')
        exists = 'true' if self.vivado_bin.exists() or shutil.which('vivado') else 'false'
        info['executable_exists'] = exists

        # Try to get actual version by calling vivado -version if possible
        try:
            if self.is_windows:
                cmd = ['cmd.exe', '/c', f'"{self.vivado_bin}" -version']
            else:
                if self.settings_script.exists():
                    cmd = ['/usr/bin/env', 'bash', '-lc',
                           f'source "{self.settings_script}" >/dev/null 2>&1 && "{self.vivado_bin}" -version']
                else:
                    # Try plain vivado in PATH
                    viv = str(
                        self.vivado_bin) if self.vivado_bin.exists() else 'vivado'
                    cmd = ['/usr/bin/env', 'bash', '-lc', f'"{viv}" -version']
            result = subprocess.run(
                cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env)
            out = (result.stdout or b'').decode('utf-8', errors='ignore')
            m = re.search(r'Vivado.*?([0-9]{4}\.[0-9]+)', out)
            if m:
                info['version'] = m.group(1)
            else:
                info['version'] = info.get('version_from_path', '')
            info['version_raw'] = out.strip()
        except Exception:
            info.setdefault('version', info.get('version_from_path', ''))
            info.setdefault('version_raw', '')

        return info
