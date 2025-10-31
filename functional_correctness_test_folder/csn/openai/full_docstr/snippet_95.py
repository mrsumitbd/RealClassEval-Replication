
import asyncio
import shlex
import os
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Union, Optional

# --------------------------------------------------------------------------- #
# Helper data structures
# --------------------------------------------------------------------------- #


@dataclass
class SubprocessResult:
    cmd: str
    returncode: int
    stdout: Optional[Union[str, bytes]]
    stderr: Optional[Union[str, bytes]]


@dataclass
class Command:
    run: List[Union[str, List[str]]]
    save: bool = False
    cwd: Optional[Union[str, Path]] = None
    bytes: bool = False
    encoding: Optional[str] = None
    stdout: Optional[Union[str, Path]] = None
    stderr: Optional[Union[str, Path]] = None
    append: bool = False


# --------------------------------------------------------------------------- #
# AsyncCmdStep implementation
# --------------------------------------------------------------------------- #

class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.
    This models a step that takes config like this in simple syntax:
        cmds:
            - <<cmd string 1>>
            - <<cmd string 2>>
    All the commands will run concurrently, in parallel.
    OR, expanded syntax is as a dict
        cmds:
