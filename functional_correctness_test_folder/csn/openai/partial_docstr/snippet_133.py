
import argparse
from typing import List, Dict, Any


class DependenciesConfiguration:
    """Dependency configuration class, for RuntimeContext.job_script_provider."""

    def __init__(self, args: argparse.Namespace) -> None:
        """Initialize with parsed command‑line arguments."""
        # Store the raw args for potential future use
        self.args: argparse.Namespace = args

        # Extract dependencies and environment variables if provided.
        # These attributes are optional; default to empty list/dict.
        self.dependencies: List[str] = getattr(args, "dependencies", [])
        self.env_vars: Dict[str, str] = getattr(args, "env", {})

    def build_job_script(self, builder: Any, command: List[str]) -> str:
        """
        Build a job script that sets up the environment, copies dependencies,
        and executes the given command.

        Parameters
        ----------
        builder : Any
            An object that may provide an ``add_line`` method and a ``build`` method.
            If such methods are not present, the script is returned as a plain string.
        command : List[str]
            The command to run in the job script.

        Returns
        -------
        str
            The complete job script as a string.
        """
        # Helper to escape shell arguments
        def _escape(arg: str) -> str:
            return arg.replace('"', '\\"')

        # Start building the script lines
        script_lines: List[str] = [
            "#!/usr/bin/env bash",
            "set -e",
        ]

        # Export environment variables
        for key, value in self.env_vars.items():
            script_lines.append(f'export {key}="{_escape(value)}"')

        # Copy dependencies into the working directory
        for dep in self.dependencies:
            script_lines.append(f'cp -r "{_escape(dep)}" .')

        # Append the actual command
        script_lines.append(" ".join(command))

        # If the builder supports incremental construction, use it
        if hasattr(builder, "add_line") and hasattr(builder, "build"):
            for line in script_lines:
                builder.add_line(line)
            return builder.build()

        # Fallback: return the script as a single string
        return "\n".join(script_lines)
