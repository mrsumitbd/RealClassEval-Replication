from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any
    # Placeholder for type checking; actual class should be provided by the caller's environment.

    class YamlAgentDocument:  # type: ignore
        pass


class AgentInfo:
    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: ModuleType | None = None,
        yaml_document: 'YamlAgentDocument | None' = None,
    ) -> None:
        self.name = name
        self.description = description
        self._file_path: Optional[Path] = file_path
        self._module: Optional[ModuleType] = module
        self._yaml_document: Optional['YamlAgentDocument'] = yaml_document

        if (module is None) == (yaml_document is None):
            # Must provide exactly one of module or yaml_document
            raise ValueError(
                "Provide exactly one of 'module' or 'yaml_document'.")

    @property
    def kind(self) -> Literal['python', 'yaml']:
        return 'python' if self._module is not None else 'yaml'

    @property
    def path(self) -> str:
        # Explicit file_path wins
        if self._file_path is not None:
            return str(self._file_path)

        # Try derive from python module
        if self._module is not None:
            mod = self._module
            p = getattr(mod, "__file__", None)
            if p:
                return str(p)
            spec = getattr(mod, "__spec__", None)
            origin = getattr(
                spec, "origin", None) if spec is not None else None
            if origin:
                return str(origin)
            name = getattr(mod, "__name__", None)
            return str(name) if name is not None else ""

        # Try derive from yaml document
        doc = self._yaml_document
        if doc is not None:
            for attr in ("file_path", "path", "source_path", "source", "uri"):
                val = getattr(doc, attr, None)
                if val:
                    try:
                        return str(val if isinstance(val, (str, Path)) else Path(str(val)))
                    except Exception:
                        continue
        return ""
