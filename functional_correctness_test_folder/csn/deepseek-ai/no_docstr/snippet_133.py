
import argparse
from typing import List


class DependenciesConfiguration:

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def build_job_script(self, builder: 'Builder', command: List[str]) -> str:
        script_lines = []
        script_lines.append("#!/bin/bash")
        script_lines.extend(builder.get_setup_commands())
        script_lines.append(" ".join(command))
        return "\n".join(script_lines)
