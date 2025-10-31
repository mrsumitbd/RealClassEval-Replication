
import subprocess
from typing import List, Dict, Union, Optional


class S2Image:
    """
    A small helper wrapper around the `s2i` (Source‑to‑Image) command line tool.
    """

    def __init__(self, s2i_path: str = "s2i") -> None:
        """
        Parameters
        ----------
        s2i_path : str, optional
            Path to the `s2i` executable. Defaults to ``"s2i"`` which assumes
            the binary is on the system ``PATH``.
        """
        self.s2i_path = s2i_path

    def extend(
        self,
        source: str,
        new_image_name: str,
        s2i_args: Optional[Union[List[str], Dict[str, str], str]] = None,
    ) -> str:
        """
        Build a new image from the given source using the `s2i` tool.

        Parameters
        ----------
        source : str
            Path to the source directory or a Git URL.
        new_image_name : str
            Desired name of the resulting image.
        s2i_args : list | dict | str, optional
            Additional arguments to pass to `s2i`. If a dictionary is supplied,
            it is converted to ``key=value`` pairs. If a string is supplied,
            it is treated as a single argument.

        Returns
        -------
        str
            The standard output produced by the `s2i` command.

        Raises
        ------
        RuntimeError
            If the `s2i` command exits with a non‑zero status.
        TypeError
            If ``s2i_args`` is not one of the accepted types.
        """
        if s2i_args is None:
            s2i_args = []

        # Normalise the arguments
        if isinstance(s2i_args, dict):
            s2i_args = [f"{k}={v}" for k, v in s2i_args.items()]
        elif isinstance(s2i_args, str):
            s2i_args = [s2i_args]
        elif not isinstance(s2i_args, list):
            raise TypeError(
                "s2i_args must be a list, dict, or str, got "
                f"{type(s2i_args).__name__}"
            )

        cmd = [self.s2i_path, "build", source, new_image_name] + s2i_args

        result = subprocess.run(
            cmd, capture_output=True, text=True, check=False
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"s2i build failed (exit {result.returncode}):\n{result.stderr}"
            )

        return result.stdout

    def usage(self) -> None:
        """
        Print a short help message describing how to use the :class:`S2Image`
        wrapper.
        """
        help_msg = (
            "S2Image helper\n"
            "==============\n"
            "Methods\n"
            "-------\n"
            "extend(source, new_image_name, s2i_args=None)\n"
            "    Build a new image using the Source‑to‑Image tool.\n"
            "    Parameters:\n"
            "        source (str): Path to source code or Git URL.\n"
            "        new_image_name (str): Desired image name.\n"
            "        s2i_args (list|dict|str, optional): Extra arguments for s2i.\n"
            "\n"
            "usage()\n"
            "    Print this help message.\n"
        )
        print(help_msg)
