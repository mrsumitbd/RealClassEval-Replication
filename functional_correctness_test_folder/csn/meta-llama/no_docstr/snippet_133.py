
import argparse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builder import Builder


class DependenciesConfiguration:

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        script = "#!/bin/bash\n"
        script += builder.get_dependencies_installation_script() + "\n"
        script += " ".join(command)
        return script
