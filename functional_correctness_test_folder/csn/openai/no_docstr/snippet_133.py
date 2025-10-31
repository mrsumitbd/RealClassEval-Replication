
import argparse
from typing import List, Dict, Any


class DependenciesConfiguration:
    """
    Handles dependency installation and job script generation.

    Parameters
    ----------
    args : argparse.Namespace
        Namespace containing optional dependency configuration arguments.
        Supported attributes (all optional):
            - requirements_file : str
                Path to a pip requirements file.
            - conda_env_file : str
                Path to a conda environment YAML file.
            - pip_packages : List[str]
                List of pip packages to install.
            - conda_packages : List[str]
                List of conda packages to install.
            - env_vars : Dict[str, str]
                Environment variables to export before running the job.
    """

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.requirements_file: str | None = getattr(
            args, "requirements_file", None)
        self.conda_env_file: str | None = getattr(args, "conda_env_file", None)
        self.pip_packages: List[str] | None = getattr(
            args, "pip_packages", None)
        self.conda_packages: List[str] | None = getattr(
            args, "conda_packages", None)
        self.env_vars: Dict[str, str] | None = getattr(args, "env_vars", {})

    def build_job_script(self, builder: Any, command: List[str]) -> str:
        """
        Build a shell script that installs dependencies and runs the given command.

        Parameters
        ----------
        builder : Any
            An object that may provide context such as the working directory.
            If it has a ``get_working_dir`` method, the script will change to that
            directory before executing the command.
        command : List[str]
            The command to run, split into a list of arguments.

        Returns
        -------
        str
            The complete job script as a string.
        """
        script_lines: List[str] = []

        # Export environment variables
        if self.env_vars:
            for key, value in self.env_vars.items():
                script_lines.append(f"export {key}={value}")

        # Change to the builder's working directory if available
        if hasattr(builder, "get_working_dir"):
            try:
                cwd = builder.get_working_dir()
                if cwd:
                    script_lines.append(f"cd {cwd}")
            except Exception:
                pass

        # Conda environment creation and activation
        if self.conda_env_file:
            script_lines.append(f"conda env create -f {self.conda_env_file}")
            # Attempt to activate the environment based on the YAML file name
            env_name = (
                self.conda_env_file.split("/")[-1].split(".")[0]
                if "/" in self.conda_env_file
                else self.conda_env_file.split(".")[0]
            )
            script_lines.append(f"conda activate {env_name}")

        # Install pip packages from requirements file
        if self.requirements_file:
            script_lines.append(f"pip install -r {self.requirements_file}")

        # Install additional pip packages
        if self.pip_packages:
            script_lines.append(f"pip install {' '.join(self.pip_packages)}")

        # Install conda packages
        if self.conda_packages:
            script_lines.append(
                f"conda install -y {' '.join(self.conda_packages)}")

        # Finally, run the command
        script_lines.append(" ".join(command))

        return "\n".join(script_lines)
