
from __future__ import annotations

import pydantic
from pydantic import BaseModel
from typing import Any, Callable, Dict, Tuple


class NoDefaultsMixin:
    """
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    """

    @pydantic.model_serializer(mode="wrap")
    def _workaround_for_design_flaw_in_pydantic(
        self, nxt: Callable[[], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Workaround for a design flaw in Pydantic that forces users to accept
        unnecessary garbage in their serialized JSON data or to override
        poorly-documented serialization hooks repeatedly. Automates overriding
        said poorly-documented serialization hooks for a single dataclass.
        """
        # Get the original serialized dict
        data = nxt()

        # Determine which fields to keep even if they are default
        keep = set(self._keep_these_fields())

        # Build a new dict excluding default values
        cleaned: Dict[str, Any] = {}
        for key, value in data.items():
            # Skip keys that are explicitly kept
            if key in keep:
                cleaned[key] = value
                continue

            # Try to get the field definition from the model
            field_def = getattr(self, "__fields__", {}).get(key)
            if field_def is None:
                # If we can't find the field definition, keep the value
                cleaned[key] = value
                continue

            # Determine the default value for the field
            default = field_def.default
            if default is pydantic.fields.Undefined:
                # If no default, keep the value
                cleaned[key] = value
                continue

            # If the field has a default factory, compute the default
            if field_def.default_factory is not pydantic.fields.Undefined:
                try:
                    default = field_def.default_factory()
                except Exception:
                    # If the factory fails, keep the value
                    cleaned[key] = value
                    continue

            # Skip the field if the value equals the default
            if value == default:
                continue

            cleaned[key] = value

        return cleaned

    def _keep_these_fields(self) -> Tuple[str, ...]:
        """
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        """
        return ()
