
import pydantic
from typing import Any, Dict, Tuple


class NoDefaultsMixin:
    """
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    """

    @pydantic.model_serializer(mode="wrap")
    def _workaround_for_design_flaw_in_pydantic(self, nxt: Any) -> Dict[str, Any]:
        """
        Workaround for a design flaw in Pydantic that forces users to accept
        unnecessary garbage in their serialized JSON data or to override poorly-documented
        serialization hooks repeatedly. Automates overriding said poorly-documented
        serialization hooks for a single dataclass.

        The serializer calls the default serializer (`nxt`) to obtain the full
        dictionary representation of the model, then removes any key whose value
        matches the field's default value, unless the key is explicitly listed
        in :meth:`_keep_these_fields`.

        Returns:
            A dictionary containing only the non-default fields (plus any
            explicitly kept fields).
        """
        # Get the full dict representation from the default serializer
        data: Dict[str, Any] = nxt()

        # Retrieve the model's field definitions
        fields = getattr(self.__class__, "model_fields", {})

        # Determine which fields to keep even if they are default
        keep = set(self._keep_these_fields())

        # Build a new dict excluding default-valued fields not in keep
        cleaned: Dict[str, Any] = {}
        for key, value in data.items():
            field = fields.get(key)
            if field is None:
                # Field not defined in the model; keep it
                cleaned[key] = value
                continue

            # Determine the default value for the field
            default = field.default
            has_default = default is not pydantic.fields.Undefined

            # If the field has a default factory, we cannot reliably compare
            if field.default_factory is not pydantic.fields.Undefined:
                # Keep the field if it's in the keep list; otherwise, drop it
                if key in keep:
                    cleaned[key] = value
                continue

            # If the field has a default and the value matches it, drop unless kept
            if has_default and value == default and key not in keep:
                continue

            # Otherwise, keep the field
            cleaned[key] = value

        return cleaned

    def _keep_these_fields(self) -> Tuple[str, ...]:
        """
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON. This is necessary for round-tripping to
        JSON when there are fields that determine which dataclass to use for
        deserialization.

        Returns:
            A tuple of field names that should be preserved in the serialized
            output even if they match their default values.
        """
        return ()
