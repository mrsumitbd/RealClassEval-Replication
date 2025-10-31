
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    """
    Persistently store and retrieve the last used parameters for a Settings object.
    The parameters are saved as JSON in a file named `last_used_params.json` inside
    the provided configuration directory (or a default one if none is supplied).
    """

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """
        Initialise the LastUsedParams instance.

        Parameters
        ----------
        config_dir : Optional[Path]
            Directory where the JSON file will be stored. If None, a default
            directory is used: ``Path.home() / ".config" / "last_used_params"``.
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "last_used_params"
        self.config_dir: Path = Path(config_dir).expanduser().resolve()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path: Path = self.config_dir / "last_used_params.json"

    def save(self, settings: "Settings") -> None:
        """
        Persist the provided settings to the JSON file.

        Parameters
        ----------
        settings : Settings
            The settings object whose state should be saved. The object is
            expected to expose either a ``to_dict`` method or a ``__dict__``
            attribute containing serialisable data.
        """
        # Extract serialisable data from the settings object
        if hasattr(settings, "to_dict") and callable(settings.to_dict):
            data = settings.to_dict()
        else:
            data = getattr(settings, "__dict__", {})

        # Ensure all values are JSON serialisable
        try:
            json.dumps(data)
        except (TypeError, OverflowError) as exc:
            raise ValueError("Settings contain non-serialisable data") from exc

        # Write to file
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)

    def load(self) -> Dict[str, Any]:
        """
        Load the last used parameters from the JSON file.

        Returns
        -------
        Dict[str, Any]
            The dictionary of parameters. If the file does not exist or is
            empty/corrupt, an empty dictionary is returned.
        """
        if not self.file_path.is_file():
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as fp:
                data = json.load(fp)
                if isinstance(data, dict):
                    return data
                # If the file contains something else, ignore it
                return {}
        except (json.JSONDecodeError, OSError):
            return {}

    def clear(self) -> None:
        """
        Remove the stored parameters file if it exists.
        """
        try:
            if self.file_path.is_file():
                self.file_path.unlink()
        except OSError:
            pass

    def exists(self) -> bool:
        """
        Check whether the parameters file exists.

        Returns
        -------
        bool
            True if the file exists, False otherwise.
        """
        return self.file_path.is_file()
