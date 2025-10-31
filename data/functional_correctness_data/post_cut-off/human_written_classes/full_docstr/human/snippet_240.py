import subprocess
from dataclasses import dataclass

@dataclass
class Volume:
    """Volume class to wrap Docker volumes."""
    name: str
    attrs: dict

    @classmethod
    def from_dict(cls, json_dict: dict) -> 'Volume':
        """Create an Image object from a json dictionary.

        Params:
            json_dict: The json dictionary to create the object from.

        Returns:
            The created volume object.
        """
        return cls(name=json_dict.get('Name', None), attrs=json_dict)

    def remove(self, force: bool=False) -> None:
        """Remove a Docker volume.

        Params:
            force: If True, force the removal of the volume.
        """
        docker = _get_docker_executable()
        try:
            _ = subprocess.run([*docker, 'volume', 'rm', '--force' if force else '', self.name], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as ex:
            raise NotFound(f'Error removing volume {self.name}: {ex}') from ex