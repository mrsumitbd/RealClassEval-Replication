from __future__ import annotations

import os
import shlex
import sys
import threading
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, Popen, PIPE


class App:
    '''App class that keep runtime status.'''

    def __init__(self, path: Path) -> None:
        '''Create a new app instance.
        Args:
            path: The path to the project.
        '''
        self.path = Path(path).resolve()

    def run_command(
        self,
        cmd: str | list[str],
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
        *,
        debug: bool = False,
        echo: bool = False,
        quiet: bool = False,
        check: bool = False,
        command_borders: bool = False
    ) -> CompletedProcess[str]:
        '''Execute the given command and returns None.
        Args:
            cmd: A list of strings containing the command to run.
            env: A dict containing the shell's environment.
            cwd: An optional Path to the working directory.
            debug: An optional bool to toggle debug output.
            echo: An optional bool to toggle command echo.
            quiet: An optional bool to toggle command output.
            check: An optional bool to toggle command error checking.
            command_borders: An optional bool to enable borders around command output.
        Returns:
            A completed process object.
        Raises:
            CalledProcessError: If return code is nonzero and check is True.
        '''
        if isinstance(cmd, str):
            args: list[str] = shlex.split(cmd)
            cmd_display = cmd
        else:
            args = list(cmd)
            cmd_display = " ".join(shlex.quote(a) for a in args)

        working_dir = Path(cwd) if cwd is not None else self.path

        # Prepare environment
        if env is not None:
            proc_env = os.environ.copy()
            proc_env.update(env)
        else:
            proc_env = os.environ.copy()

        if echo and not quiet:
            print(f"+ {cmd_display}", flush=True)

        if debug and not quiet:
            print(f"[debug] cwd: {working_dir}", flush=True)
            if env:
                for k, v in env.items():
                    print(f"[debug] env {k}={v}", flush=True)

        if command_borders and not quiet:
            border = "=" * max(10, min(80, len(cmd_display) + 10))
            print(border, flush=True)
            print(f"# Running: {cmd_display}", flush=True)
            print(border, flush=True)

        # Run process with streaming and capture
        proc = Popen(
            args,
            cwd=str(working_dir),
            env=proc_env,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,
        )

        stdout_chunks: list[str] = []
        stderr_chunks: list[str] = []

        def _reader(stream, sink, collect_list, is_stdout: bool):
            for line in iter(stream.readline, ""):
                collect_list.append(line)
                if not quiet:
                    sink.write(line)
                    sink.flush()
            stream.close()

        threads: list[threading.Thread] = []
        t_out = threading.Thread(target=_reader, args=(
            proc.stdout, sys.stdout, stdout_chunks, True))
        t_err = threading.Thread(target=_reader, args=(
            proc.stderr, sys.stderr, stderr_chunks, False))
        t_out.start()
        t_err.start()
        threads.extend([t_out, t_err])

        rc = proc.wait()
        for t in threads:
            t.join()

        stdout_text = "".join(stdout_chunks)
        stderr_text = "".join(stderr_chunks)

        if command_borders and not quiet:
            end_border = "-" * 20
            print(f"{end_border} exit {rc} {end_border}", flush=True)

        if check and rc != 0:
            raise CalledProcessError(
                rc, args, output=stdout_text, stderr=stderr_text)

        return CompletedProcess(args=args, returncode=rc, stdout=stdout_text, stderr=stderr_text)
