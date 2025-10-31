
import argparse


class DependenciesConfiguration:

    def __init__(self, args: argparse.Namespace) -> None:
        self.dependencies = getattr(args, 'dependencies', [])
        self.env_vars = getattr(args, 'env_vars', {})
        self.modules = getattr(args, 'modules', [])

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        lines = []
        # Load modules if any
        for module in self.modules:
            lines.append(f"module load {module}")
        # Set environment variables if any
        for key, value in self.env_vars.items():
            lines.append(f"export {key}={value}")
        # Install dependencies if any
        if self.dependencies:
            lines.append(f"pip install {' '.join(self.dependencies)}")
        # Add the command to run
        lines.append(' '.join(command))
        return '\n'.join(lines)
