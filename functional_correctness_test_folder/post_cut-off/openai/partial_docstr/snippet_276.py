
import pydantic
from pydantic import BaseModel, Field
from typing import Any, Dict, Tuple


class NoDefaultsMixin:
    """
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    """

    @pydantic.model_serializer(mode="wrap")
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        """
        Wraps the default serializer to strip out fields that are set to their
        default values, unless the field is explicitly listed in
        `_keep_these_fields`. This helps keep the JSON representation concise
        while still allowing round‑tripping for fields that influence
        deserialization.
        """
        # Get the default serialized representation
        data: Dict[str, Any] = nxt()

        # If the model is a BaseModel, we can inspect its fields
        if isinstance(self, BaseModel):
            keep = set(self._keep_these_fields())
            for key, field in self.model_fields.items():
                # Skip keys that are explicitly kept
                if key in keep:
                    continue

                # Determine the default value for the field
                default = field.default
                # If the field has no default, keep it
                if default is pydantic.fields.Undefined:
                    continue

                # If the current value equals the default, drop it
                if key in data and data[key] == default:
                    data.pop(key, None)

        return data

    def _keep_these_fields(self) -> Tuple[str, ...]:
        """
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON. This is necessary for round‑tripping
        to JSON when there are fields that determine which dataclass to use for
        deserialization.
        """
        return ()
