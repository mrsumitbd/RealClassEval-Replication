import os
import sys
import zlib
import tempfile
import subprocess
from typing import Optional, Union, List, Any


class WebProcessMixin:
    def start_web_ui_direct(self, app_context: Any, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        pid_path = self.get_web_ui_pid_path()

        def _is_running(pid: int) -> bool:
            if pid <= 0:
                return False
            try:
                if os.name == "nt":
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                    handle = kernel32.OpenProcess(
                        PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
                    if not handle:
                        return False
                    try:
                        exit_code = ctypes.c_uint()
                        if kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)) == 0:
                            return False
                        return exit_code.value == 259  # STILL_ACTIVE
                    finally:
                        kernel32.CloseHandle(handle)
                else:
                    os.kill(pid, 0)
                    return True
            except Exception:
                return False

        if os.path.isfile(pid_path):
            try:
                with open(pid_path, "r", encoding="utf-8") as f:
                    existing_pid = int(f.read().strip())
                if _is_running(existing_pid):
                    return
                else:
                    os.remove(pid_path)
            except Exception:
                try:
                    os.remove(pid_path)
                except Exception:
                    pass

        exe = self.get_web_ui_executable_path()
        args = list(self.get_web_ui_expected_start_arg())

        # Heuristic support for Python's built-in http.server when used as default
        if any(part == "http.server" for part in args):
            bind_host: Optional[str] = None
            if isinstance(host, str):
                bind_host = host
            elif isinstance(host, list) and host:
                bind_host = host[0]
            if bind_host:
                args += ["--bind", bind_host]

        # Optional generic flags (may be ignored by target command)
        if host and not any(part == "http.server" for part in args):
            if isinstance(host, str):
                args += ["--host", host]
            else:
                for h in host:
                    args += ["--host", h]
        if debug:
            args += ["--debug"]
        if threads is not None:
            args += ["--threads", str(threads)]

        work_dir = (
            getattr(app_context, "work_dir", None)
            or getattr(app_context, "root_dir", None)
            or getattr(app_context, "project_dir", None)
            or os.getcwd()
        )

        popen_kwargs = {
            "cwd": work_dir,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "stdin": subprocess.DEVNULL,
            "close_fds": True,
        }

        if os.name == "nt":
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            popen_kwargs["creationflags"] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        else:
            popen_kwargs["preexec_fn"] = os.setsid  # type: ignore[arg-type]

        proc = subprocess.Popen([exe] + args, **popen_kwargs)  # noqa: S603

        try:
            with open(pid_path, "w", encoding="utf-8") as f:
                f.write(str(proc.pid))
        except Exception:
            try:
                proc.terminate()
            except Exception:
                pass
            raise

    def get_web_ui_pid_path(self) -> str:
        cwd = os.getcwd()
        uid = f"{abs(zlib.adler32(cwd.encode('utf-8')))}"
        name = f"{self.__class__.__name__}_webui_{uid}.pid"
        return os.path.join(tempfile.gettempdir(), name)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return ["-m", "http.server"]

    def get_web_ui_executable_path(self) -> str:
        return sys.executable
