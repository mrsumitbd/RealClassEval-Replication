
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    """
    Persistently store and retrieve the last used parameters for a Settings object.
    The parameters are saved as JSON in a file located in the provided configuration
    directory or, if none is provided, in the user's home directory.
    """

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """
        Initialize the LastUsedParams instance.

        Parameters
        ----------
        config_dir : Optional[Path]
            Directory where the parameters file will be stored. If None, the file
            will be stored in the user's home directory as '.last_used_params.json'.
        """
        if config_dir is None:
            self.file_path = Path.home() / ".last_used_params.json"
        else:
            self.file_path = config_dir / "last_used_params.json"

    def save(self, settings: "Settings") -> None:
        """
        Save the provided settings to the parameters file.

        Parameters
        ----------
        settings : Settings
            The settings object whose attributes should be persisted.
        """
        # Convert the settings object to a serialisable dictionary.
        # If the object has a custom to_dict method, use it; otherwise fall back to __dict__.
        if hasattr(settings, "to_dict") and callable(settings.to_dict):
            data = settings.to_dict()
        else:
            data = settings.__dict__

        # Ensure the parent directory exists.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the data as JSON.
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def load(self) -> Dict[str, Any]:
        """
        Load the last used parameters from the file.

        Returns
        -------
        Dict[str, Any]
            The dictionary of parameters. If the file does not exist or is
            malformed, an empty dictionary is returned.
        """
        if not self.file_path.exists():
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # If the file is corrupted or unreadable, treat it as empty.
            return {}

    def clear(self) -> None:
        """
        Remove the parameters file if it exists.
        """
        if self.file_path.exists():
            try:
                self.file_path.unlink()
            except OSError:
                # If the file cannot be deleted, ignore the error.
                pass

    def exists(self) -> bool:
        """
        Check whether the parameters file exists.

        Returns
        -------
        bool
            True if the file exists, False otherwise.
        """
        return self.file_path.exists()
