from typing import Dict, Any, Optional
import os
import sys
import platform
import datetime
import subprocess
import shlex
import shutil
from pathlib import Path


class ScriptRunner:

    def __init__(self, log_path: str = 'data/local_logs/train.log'):
        self.default_log_path = log_path
        log_dir = Path(log_path).expanduser().resolve().parent
        log_dir.mkdir(parents=True, exist_ok=True)

    def _prepare_log_file(self, script_type: str) -> str:
        base = Path(self.default_log_path).expanduser().resolve()
        log_dir = base.parent
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_type = (script_type or "script").strip().replace(" ", "_")
        log_name = f"{safe_type}_{ts}.log"
        log_path = log_dir / log_name
        # Touch the file
        log_path.touch(exist_ok=True)
        return str(log_path)

    def _check_execution_env(self) -> Dict[str, str]:
        return {
            "os": os.name,
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "cwd": str(Path.cwd()),
            "env_vars_count": str(len(os.environ)),
        }

    def _check_python_version(self) -> str:
        return sys.version

    def execute_script(self, script_path: str, script_type: str, is_python: bool = False, args: Optional[list] = None) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "command": None,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "log_path": None,
            "env": self._check_execution_env(),
            "python_version": self._check_python_version(),
            "error": None,
        }

        if args is None:
            args = []

        script_path = str(Path(script_path).expanduser())
        if not os.path.exists(script_path):
            result["error"] = f"Script not found: {script_path}"
            return result

        log_path = self._prepare_log_file(script_type)
        result["log_path"] = log_path

        cmd: list = []
        if is_python:
            cmd = [sys.executable, script_path] + [str(a) for a in args]
        else:
            # If it's a shell script on non-Windows, prefer bash if available
            if script_path.endswith(".sh"):
                bash = shutil.which("bash")
                if bash:
                    cmd = [bash, script_path] + [str(a) for a in args]
                else:
                    cmd = [script_path] + [str(a) for a in args]
            else:
                # Generic executable or command
                # If script_path is a file ensure it's executable or run via shell=False
                # For commands not as path, try which
                if os.path.isfile(script_path):
                    cmd = [script_path] + [str(a) for a in args]
                else:
                    which = shutil.which(script_path)
                    if which:
                        cmd = [which] + [str(a) for a in args]
                    else:
                        # Fallback: run via shell
                        cmd_str = " ".join(
                            [shlex.quote(script_path)] + [shlex.quote(str(a)) for a in args])
                        result["command"] = cmd_str
                        try:
                            completed = subprocess.run(
                                cmd_str,
                                shell=True,
                                capture_output=True,
                                text=True,
                                check=False,
                            )
                            result["returncode"] = completed.returncode
                            result["stdout"] = completed.stdout
                            result["stderr"] = completed.stderr
                        except Exception as e:
                            result["error"] = str(e)
                        finally:
                            try:
                                with open(log_path, "a", encoding="utf-8") as f:
                                    f.write(f"COMMAND: {cmd_str}\n")
                                    f.write(result["stdout"] or "")
                                    if result["stderr"]:
                                        f.write("\n--- STDERR ---\n")
                                        f.write(result["stderr"])
                                    f.write("\n")
                            except Exception:
                                pass
                        return result

        result["command"] = " ".join(shlex.quote(c) for c in cmd)

        try:
            completed = subprocess.run(
                cmd,
                shell=False,
                capture_output=True,
                text=True,
                check=False,
            )
            result["returncode"] = completed.returncode
            result["stdout"] = completed.stdout
            result["stderr"] = completed.stderr
        except FileNotFoundError as e:
            result["error"] = f"Executable not found: {e}"
        except PermissionError as e:
            result["error"] = f"Permission error: {e}"
        except Exception as e:
            result["error"] = str(e)
        finally:
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"COMMAND: {result['command']}\n")
                    f.write(result["stdout"] or "")
                    if result["stderr"]:
                        f.write("\n--- STDERR ---\n")
                        f.write(result["stderr"])
                    f.write("\n")
            except Exception:
                pass

        return result
