
import os
import re
import subprocess
from typing import Optional


class Shell:
    '''Wrapper around subprocess supporting dry_run mode.'''

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        '''Initialize shell wrapper.
        Args:
            dry_run: If True, commands will be logged but not executed
            safe_mode: If True, enables additional safety checks for commands
        '''
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        '''Validate command for basic safety if safe_mode is enabled.
        Args:
            cmd: Command to validate
        Raises:
            RuntimeError: If command appears unsafe
        '''
        if not self.safe_mode:
            return

        # Very simple safety checks – look for dangerous patterns
        dangerous_patterns = [
            r'\brm\s+-rf\b',
            r'\brm\s+-r\b',
            r'\brm\s+-f\b',
            r'\bshutdown\b',
            r'\breboot\b',
            r'\bhalt\b',
            r'\bpoweroff\b',
            r'\bmkfs\b',
            r'\bdd\b',
            r'\bchmod\b',
            r'\bchown\b',
            r'\bmv\b',
            r'\bln\b',
            r'\bsudo\b',
            r'\bapt\b',
            r'\byum\b',
            r'\bapt-get\b',
            r'\baptitude\b',
            r'\bdnf\b',
            r'\bpacman\b',
            r'\bbrew\b',
            r'\bgem\b',
            r'\bpip\b',
            r'\bpython\b',
            r'\bperl\b',
            r'\bnode\b',
            r'\bnpm\b',
            r'\bgo\b',
            r'\bmake\b',
            r'\bcmake\b',
            r'\bdocker\b',
            r'\bkubectl\b',
            r'\bterraform\b',
            r'\bansible\b',
            r'\bchef\b',
            r'\bpuppet\b',
        ]

        for pat in dangerous_patterns:
            if re.search(pat, cmd, re.IGNORECASE):
                raise RuntimeError(f"Unsafe command detected: {cmd!r}")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str]
