from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass
class DependencyInfo:
    """Information about project dependencies."""
    file: Optional[str]
    type: str
    resolved_path: Optional[str] = None
    install_path: Optional[str] = None

    @property
    def found(self) -> bool:
        """Whether a dependency file was found."""
        return self.file is not None

    @property
    def is_pyproject(self) -> bool:
        """Whether this is a pyproject.toml file."""
        return self.type == 'pyproject'

    @property
    def is_requirements(self) -> bool:
        """Whether this is a requirements file."""
        return self.type == 'requirements'

    @property
    def is_root_package(self) -> bool:
        """Whether this dependency points to the root package."""
        return self.is_pyproject and self.install_path == '.'