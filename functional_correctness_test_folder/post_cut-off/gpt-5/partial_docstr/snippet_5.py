from __future__ import annotations

import os
import sys
import platform
import subprocess
import threading
import datetime
from typing import Dict, Any, Optional, List


class ScriptRunner:
    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.base_log_path = log_path
        self._last_log_path: Optional[str] = None
        # Ensure base directory exists
        base_dir = os.path.dirname(self.base_log_path) or "."
        os.makedirs(base_dir, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        base_dir = os.path.dirname(self.base_log_path) or "."
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(self.base_log_path))[0]
        ext = os.path.splitext(self.base_log_path)[1] or ".log"
        safe_type = "".join(c if c.isalnum() or c in (
            "-", "_") else "_" for c in (script_type or "script"))
        log_filename = f"{base_name}_{safe_type}_{timestamp}{ext}"
        log_path = os.path.join(base_dir, log_filename)
        self._last_log_path = log_path
        return log_path

    def _check_execution_env(self) -> Dict[str, str]:
        def _in_docker() -> bool:
            try:
                if os.path.exists("/.dockerenv"):
                    return True
                cgroup_path = "/proc/1/cgroup"
                if os.path.exists(cgroup_path):
                    with open(cgroup_path, "rt", encoding="utf-8", errors="ignore") as f:
                        data = f.read()
                    tokens = ("docker", "kubepods", "containerd", "podman")
                    return any(t in data.lower() for t in tokens)
            except Exception:
                pass
            env_flags = ("DOCKER_CONTAINER", "container",
                         "AM_I_IN_A_DOCKER_CONTAINER")
            return any(os.environ.get(k, "").strip() for k in env_flags)

        env_type = "docker" if _in_docker() else "system"
        details: Dict[str, str] = {
            "environment": env_type,
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "",
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "cwd": os.getcwd(),
        }
        return details

    def _check_python_version(self) -> str:
        return platform.python_version()

    def execute_script(
        self,
        script_path: str,
        script_type: str,
        is_python: bool = False,
        args: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        args = args or []
        log_path = self._prepare_log_file(script_type)
        env_info = self._check_execution_env()
        py_version = self._check_python_version()

        if not script_path:
            return {
                "success": False,
                "error": "Empty script_path",
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "log_path": log_path,
                "command": [],
                "environment": env_info,
                "python_version": py_version,
            }

        def build_command() -> List[str]:
            if is_python:
                return [sys.executable, script_path, *args]
            # Non-python: try to execute directly if executable
            if os.access(script_path, os.X_OK):
                return [script_path, *args]
            system = platform.system()
            if system == "Windows":
                # Use cmd to run batch or other scripts
                return ["cmd", "/c", script_path, *args]
            # On POSIX, prefer bash if not executable
            sh = "/bin/bash" if os.path.exists("/bin/bash") else "/bin/sh"
            return [sh, script_path, *args]

        cmd = build_command()

        stdout_lines: List[str] = []
        stderr_lines: List[str] = []

        def _stream_reader(pipe, collector: List[str], log_file, prefix: str):
            try:
                for line in iter(pipe.readline, ''):
                    if not line:
                        break
                    collector.append(line)
                    try:
                        log_file.write(f"{prefix}{line}")
                        log_file.flush()
                    except Exception:
                        pass
            except Exception as e:
                try:
                    msg = f"{prefix}[streaming error] {e}\n"
                    collector.append(msg)
                    log_file.write(msg)
                    log_file.flush()
                except Exception:
                    pass
            finally:
                try:
                    pipe.close()
                except Exception:
                    pass

        header = (
            f"===== ScriptRunner Execution =====\n"
            f"Timestamp: {datetime.datetime.now().isoformat()}\n"
            f"Script: {script_path}\n"
            f"Type: {script_type}\n"
            f"Command: {' '.join(repr(c) for c in cmd)}\n"
            f"Environment: {env_info.get('environment')}\n"
            f"OS: {env_info.get('os')} {env_info.get('os_release')} ({env_info.get('machine')})\n"
            f"Python: {py_version} ({env_info.get('python_executable')})\n"
            f"WorkingDir: {env_info.get('cwd')}\n"
            f"==================================\n"
        )

        try:
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(header)
                lf.flush()

                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    bufsize=1,
                    cwd=None,
                    env=os.environ.copy()
                )

                t_out = threading.Thread(target=_stream_reader, args=(
                    proc.stdout, stdout_lines, lf, "[OUT] "), daemon=True)
                t_err = threading.Thread(target=_stream_reader, args=(
                    proc.stderr, stderr_lines, lf, "[ERR] "), daemon=True)
                t_out.start()
                t_err.start()

                returncode = proc.wait()
                t_out.join(timeout=1.0)
                t_err.join(timeout=1.0)

                footer = (
                    "\n===== Execution Finished =====\n"
                    f"Return code: {returncode}\n"
                    "================================\n"
                )
                lf.write(footer)
                lf.flush()

            stdout_str = "".join(stdout_lines)
            stderr_str = "".join(stderr_lines)

            return {
                "success": returncode == 0,
                "returncode": returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "log_path": log_path,
                "command": cmd,
                "environment": env_info,
                "python_version": py_version,
            }
        except FileNotFoundError as e:
            err_msg = f"Command component not found: {e}"
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(f"[ERR] {err_msg}\n")
            return {
                "success": False,
                "error": err_msg,
                "returncode": None,
                "stdout": "",
                "stderr": err_msg,
                "log_path": log_path,
                "command": cmd,
                "environment": env_info,
                "python_version": py_version,
            }
        except Exception as e:
            err_msg = f"Execution failed: {e}"
            try:
                with open(log_path, "a", encoding="utf-8") as lf:
                    lf.write(f"[ERR] {err_msg}\n")
            except Exception:
                pass
            return {
                "success": False,
                "error": err_msg,
                "returncode": None,
                "stdout": "",
                "stderr": err_msg,
                "log_path": log_path,
                "command": cmd,
                "environment": env_info,
                "python_version": py_version,
            }
